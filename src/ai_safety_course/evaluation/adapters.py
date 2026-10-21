"""adapters — deterministic, offline model adapters for the P01 harness.

An adapter is the harness's stand-in for "the system under evaluation".
The three shipped adapters are deliberately local and deterministic:

* :class:`ScriptedAdapter` — returns a fixed response per case id, read
  from a lookup table. This is the CPU-only instrument used for the
  committed example run and for regression tests.
* :class:`EchoAdapter` — returns the prompt verbatim; a never-refuses
  baseline that brackets the ledger from below.
* :class:`CallableAdapter` — wraps a plain Python callable for programmatic
  use (local rule functions, or future local-model wrappers added with the
  repository's planned ``ml`` dependency group — never constructed from
  YAML config, since callables are not serializable).

No adapter performs network access or model downloads: the harness runs
on CPU-only machines in bounded time by construction. Adapters receive
the run ``seed`` on every call so that any stochastic component *could*
be seeded deterministically even when one is added later.
"""

import hashlib
import json
from collections.abc import Callable, Mapping
from typing import Any, Protocol


class AdapterError(RuntimeError):
    """Raised when an adapter is misconfigured or a lookup fails (fail-closed)."""


class ModelAdapter(Protocol):
    """Protocol every P01 model adapter implements.

    ``generate`` must be deterministic given the same prompt, case id, and
    seed: the runner byte-compares repeated runs, so any injected noise
    must be derived from the seed.
    """

    name: str

    def generate(self, prompt: str, *, case_id: str, seed: int) -> str:
        """Return the adapter's response text for ``prompt``."""
        ...


class ScriptedAdapter:
    """Deterministic adapter answering from a case-id → response lookup.

    Fail-closed: asking for a case id that is not in the lookup raises
    :class:`AdapterError` — the harness never invents a default response,
    because an invented response would silently corrupt the ledger.
    """

    def __init__(self, responses: Mapping[str, str], name: str = "scripted") -> None:
        """Build from a mapping of case id to response text.

        Args:
            responses: the lookup table; keys and values must be non-empty
                strings.
            name: adapter display name.

        Raises:
            AdapterError: if ``responses`` is empty or malformed.
        """
        if not responses:
            raise AdapterError("ScriptedAdapter requires a non-empty responses mapping")
        for key, value in responses.items():
            if not isinstance(key, str) or not key:
                raise AdapterError(
                    f"ScriptedAdapter response key must be a non-empty string: {key!r}"
                )
            if not isinstance(value, str) or not value:
                raise AdapterError(
                    f"ScriptedAdapter response for {key!r} must be a non-empty string"
                )
        self._responses: dict[str, str] = dict(responses)
        self.name = name

    def generate(self, prompt: str, *, case_id: str, seed: int) -> str:
        """Return the scripted response for ``case_id`` (seed accepted, unused)."""
        try:
            return self._responses[case_id]
        except KeyError as exc:
            known = len(self._responses)
            raise AdapterError(
                f"ScriptedAdapter has no scripted response for case id {case_id!r} "
                f"({known} responses loaded); refusing to invent a default"
            ) from exc

    @property
    def responses(self) -> Mapping[str, str]:
        """The scripted response table (copy, to keep the adapter immutable)."""
        return dict(self._responses)


class EchoAdapter:
    """Baseline adapter that echoes the prompt back (never refuses).

    Together with an all-refuse :class:`ScriptedAdapter` it brackets the
    achievable ledger: echo shows the floor of the attack-side refusal
    rate (0) and the ceiling of safe-side compliance (100%).
    """

    def __init__(self, name: str = "echo") -> None:
        self.name = name

    def generate(self, prompt: str, *, case_id: str, seed: int) -> str:
        """Return ``prompt`` verbatim (deterministic; seed unused)."""
        return prompt


class CallableAdapter:
    """Adapter wrapping a Python callable ``fn(prompt, case_id, seed) -> str``.

    Use this for local rule-based "models" or future local-model wrappers.
    It exists for programmatic construction only; YAML configs cannot
    reference callables, and the config factory rejects them accordingly.
    """

    def __init__(self, fn: Callable[[str, str, int], str], name: str = "callable") -> None:
        if not callable(fn):
            raise AdapterError("CallableAdapter requires a callable fn(prompt, case_id, seed)")
        self._fn = fn
        self.name = name

    def generate(self, prompt: str, *, case_id: str, seed: int) -> str:
        """Delegate to the wrapped callable (exceptions propagate)."""
        return self._fn(prompt, case_id, seed)


def config_sha256(config: Mapping[str, Any]) -> str:
    """Return a stable SHA-256 fingerprint of an adapter config mapping.

    The mapping is canonicalized via sorted-key compact JSON before
    hashing, so equal configs always produce equal fingerprints regardless
    of key order or YAML formatting.
    """
    canonical = json.dumps(dict(config), sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def adapter_from_config(config: Mapping[str, Any]) -> ModelAdapter:
    """Construct an adapter from a parsed YAML adapter-config mapping.

    Supported ``kind`` values (fail-closed on anything else):

    * ``"scripted"`` — requires a ``responses`` mapping of case id to text.
    * ``"echo"`` — takes no extra configuration.

    Args:
        config: the adapter block of a run config.

    Returns:
        The constructed adapter.

    Raises:
        AdapterError: on unknown kind, missing or extra keys, or an
            invalid responses table.
    """
    if not isinstance(config, Mapping):
        raise AdapterError(f"adapter config must be a mapping, got {type(config)!r}")
    if "kind" not in config:
        raise AdapterError("adapter config is missing the 'kind' field")
    kind = config["kind"]
    extra = [key for key in config if key not in {"kind", "responses"}]

    if kind == "scripted":
        if extra:
            raise AdapterError(f"scripted adapter config has unknown fields: {extra}")
        if "responses" not in config:
            raise AdapterError("scripted adapter config requires a 'responses' mapping")
        responses = config["responses"]
        if not isinstance(responses, Mapping):
            raise AdapterError(f"scripted 'responses' must be a mapping, got {type(responses)!r}")
        return ScriptedAdapter(responses)
    if kind == "echo":
        if extra:
            raise AdapterError(f"echo adapter config has unknown fields: {extra}")
        return EchoAdapter()
    raise AdapterError(
        f"unknown adapter kind {kind!r}; supported kinds: 'scripted', 'echo' "
        "(callable adapters are programmatic-only, fail-closed by design)"
    )

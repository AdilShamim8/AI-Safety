"""Lazy loaders for registered datasets.

Loaders import Hugging Face ``datasets`` lazily so environments without
it (CI smoke tests, serverless filters) can still import this module and
inspect the registry. Each loader records provenance (dataset id +
revision) on the returned object — the repo rule from
docs/datasets/index.md: every result is attributable.
"""

from __future__ import annotations

from typing import Any

from .registry import DATASET_REGISTRY, DatasetSpec, get_spec


class DatasetUnavailableError(RuntimeError):
    """Raised when a dataset cannot be loaded (missing lib or network)."""


def load_dataset_by_name(
    name: str,
    *,
    split: str | None = None,
    revision: str | None = None,
    **kwargs: Any,
):
    """Load a registered dataset by its short name.

    Parameters
    ----------
    name      : registry key (see ``list_datasets()``)
    split     : dataset split (e.g. "train", "test"); None lets HF decide
    revision  : pin a specific revision for reproducibility; falls back to
                the spec's recorded default if present
    kwargs    : forwarded to ``datasets.load_dataset`` (e.g. ``config_name``)

    Returns
    -------
    ``datasets.Dataset`` / ``DatasetDict`` with a ``.aisafety_provenance``
    attribute recording what was loaded.
    """
    spec = get_spec(name)
    if spec.hf_id is None:
        raise DatasetUnavailableError(
            f"{name!r} is registered metadata-only: it is distributed outside "
            f"Hugging Face at {spec.source_url}. Fetch it explicitly and "
            f"verify the license ({spec.license}) before use."
        )
    try:
        from datasets import load_dataset  # lazy heavy import
    except ImportError as err:  # pragma: no cover - environment dependent
        raise DatasetUnavailableError(
            "the 'datasets' package is required for loading; "
            "pip install datasets>=2.19.0"
        ) from err

    load_kwargs: dict[str, Any] = dict(kwargs)
    if revision is not None:
        load_kwargs["revision"] = revision
    if split is not None:
        load_kwargs["split"] = split

    ds = load_dataset(spec.hf_id, **load_kwargs)
    try:  # attach provenance without subclassing
        ds.aisafety_provenance = {  # type: ignore[attr-defined]
            "name": spec.name,
            "hf_id": spec.hf_id,
            "revision": revision or "default",
            "paper": spec.paper,
            "license": spec.license,
        }
    except AttributeError:  # DatasetDict etc.
        pass
    return ds


def provenance_for(name: str) -> dict[str, str]:
    """Return the provenance record for a dataset without loading it."""
    spec: DatasetSpec = get_spec(name)
    return {
        "name": spec.name,
        "hf_id": spec.hf_id or "",
        "source_url": spec.source_url,
        "paper": spec.paper,
        "license": spec.license,
    }


def summarize_registry() -> list[dict[str, str]]:
    """Provenance records for every registered dataset (for reports)."""
    return [provenance_for(name) for name in sorted(DATASET_REGISTRY)]

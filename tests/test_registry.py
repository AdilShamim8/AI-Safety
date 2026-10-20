"""Tests for the dataset registry (metadata only — no network)."""

from __future__ import annotations

import pytest

from src.aisafety.data.registry import (
    DATASET_REGISTRY,
    get_spec,
    list_datasets,
)


class TestRegistry:
    def test_registry_nonempty(self):
        assert len(DATASET_REGISTRY) >= 15

    def test_canonical_datasets_present(self):
        for name in ("truthfulqa", "hh_rlhf", "toxigen", "bold", "bbq",
                     "mmlu", "gsm8k", "xstest", "advbench", "jailbreakbench"):
            assert name in DATASET_REGISTRY, f"missing {name}"

    def test_every_spec_has_paper_and_license(self):
        for spec in DATASET_REGISTRY.values():
            assert spec.paper.startswith("arXiv:"), spec
            assert spec.license, spec
            assert spec.source_url.startswith("http"), spec

    def test_get_spec_unknown_raises(self):
        with pytest.raises(KeyError):
            get_spec("definitely_not_registered")

    def test_get_spec_error_lists_known(self):
        try:
            get_spec("nope")
        except KeyError as err:
            assert "truthfulqa" in str(err)

    def test_list_datasets_filter(self):
        bias_sets = list_datasets("bias")
        assert any(s.name == "bold" for s in bias_sets)


class TestLoadersMetadata:
    def test_provenance_for(self):
        from src.aisafety.data.loaders import provenance_for

        prov = provenance_for("truthfulqa")
        assert prov["hf_id"] == "truthful_qa"
        assert prov["paper"] == "arXiv:2109.07958"

    def test_summarize_registry(self):
        from src.aisafety.data.loaders import summarize_registry

        records = summarize_registry()
        assert len(records) == len(DATASET_REGISTRY)
        assert all("license" in r for r in records)

    def test_metadata_only_dataset_rejected(self):
        from src.aisafety.data.loaders import (
            DatasetUnavailableError,
            load_dataset_by_name,
        )

        with pytest.raises(DatasetUnavailableError):
            load_dataset_by_name("advbench")  # GitHub-distributed only

    def test_unknown_dataset_name(self):
        from src.aisafety.data.loaders import load_dataset_by_name

        with pytest.raises(KeyError):
            load_dataset_by_name("no_such_dataset")

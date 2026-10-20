"""Dataset registry and loaders for real, public AI-safety datasets.

See docs/datasets/index.md for the full catalog with licenses and
canonical access points. Only datasets with public, canonical
distribution are registered here — no synthetic stand-ins.
"""

from __future__ import annotations

from .registry import DATASET_REGISTRY, DatasetSpec, get_spec, list_datasets
from .loaders import load_dataset_by_name

__all__ = [
    "DATASET_REGISTRY",
    "DatasetSpec",
    "get_spec",
    "list_datasets",
    "load_dataset_by_name",
]

from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

import pandas as pd
import polars as pl

from .store import FeatureSetResult, FeatureStore


__all__ = [
    "build_features_with_mlflow",
    "log_feature_metadata_to_mlflow",
    "load_features_from_mlflow",
]


def _import_mlflow():
    pass


def _require_active_run(mlflow_module, run=None):
    pass


def _parameter_prefix(prefix: Optional[str], name: str) -> str:
    pass


def build_features_with_mlflow(
    store: FeatureStore,
    name: str,
    data: Union[pd.DataFrame, pl.DataFrame],
    *,
    params: Optional[Mapping[str, Any]] = None,
    refresh: bool = False,
    version: Optional[str] = None,
    key_columns: Optional[Sequence[str]] = None,
    storage_format: Optional[str] = None,
    tags: Optional[Sequence[str]] = None,
    extra_metadata: Optional[Mapping[str, Any]] = None,
    return_engine: str = "auto",
    writer_options: Optional[Mapping[str, Any]] = None,
    params_prefix: Optional[str] = None,
    metadata_artifact_path: str = "feature_store",
    log_metadata_artifact: bool = True,
    log_feature_artifact: Optional[bool] = None,
    run=None,
    **build_kwargs: Any,
) -> FeatureSetResult:
    """
    Build (or reuse) a feature set while recording versioning metadata to MLflow.
    """
    pass


def log_feature_metadata_to_mlflow(
    *,
    result: FeatureSetResult,
    name: str,
    params_prefix: Optional[str] = None,
    metadata_artifact_path: str = "feature_store",
    log_metadata_artifact: bool = True,
    log_feature_artifact: bool = False,
) -> None:
    """
    Log feature metadata and optional artifacts for a previously built feature set.
    """
    pass


def load_features_from_mlflow(
    store: FeatureStore,
    name: str,
    *,
    run_id: Optional[str] = None,
    params_prefix: Optional[str] = None,
    version_param: Optional[str] = None,
    return_engine: str = "auto",
    strict: bool = True,
) -> FeatureSetResult:
    """
    Load a feature set using the version recorded in an MLflow run.
    """
    pass

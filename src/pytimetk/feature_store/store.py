from __future__ import annotations

import inspect
import json
import os
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import posixpath
from pathlib import Path
import time
import warnings
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    BinaryIO,
)

import pandas as pd
import polars as pl

import pyarrow.fs as pa_fs

from pytimetk.utils.dataframe_ops import identify_frame_kind, resolve_pandas_groupby_frame

_FEATURE_STORE_BETA_MESSAGE = (
    "Feature Store & Caching is currently in beta. APIs and storage formats may change before general availability."
)


def _warn_feature_store_beta() -> None:
    pass

Jsonable = Union[str, int, float, bool, None, Mapping[str, Any], Sequence[Any]]
TransformCallable = Callable[[Any], Any]


@dataclass(frozen=True)
class FeatureSetMetadata:
    """
    Immutable metadata describing a single materialised feature set.
    """

    name: str
    version: str
    cache_key: str
    storage_path: str
    storage_format: str
    storage_backend: str
    artifact_uri: str
    created_at: str
    data_fingerprint: str
    transform_fingerprint: str
    transform_module: str
    transform_name: str
    transform_kwargs: Mapping[str, Any]
    pytimetk_version: str
    package_versions: Mapping[str, str]
    tags: Tuple[str, ...] = field(default_factory=tuple)
    description: Optional[str] = None
    key_columns: Optional[Tuple[str, ...]] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    extra_metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class FeatureSetResult:
    """
    Wrapper returned by the feature store for build/load operations.
    """

    data: Union[pd.DataFrame, pl.DataFrame]
    metadata: FeatureSetMetadata
    from_cache: bool


@dataclass
class RegisteredTransform:
    name: str
    function: TransformCallable
    default_kwargs: MutableMapping[str, Any]
    description: Optional[str]
    tags: Tuple[str, ...]
    default_key_columns: Optional[Tuple[str, ...]]
    extra_metadata: Mapping[str, Any]

    def fingerprint(self, runtime_kwargs: Mapping[str, Any]) -> str:
        pass

    def _callable_signature(self) -> str:
        pass


class FileLockManager:
    """
    Lightweight file-based locking to coordinate concurrent writers.
    """

    def __init__(
        self,
        lock_dir: Path,
        *,
        timeout: float = 30.0,
        poll_interval: float = 0.2,
    ) -> None:
        self.lock_dir = lock_dir
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.lock_dir.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def acquire(self, key: str):
        pass


class ArtifactBackend:
    name: str = "base"

    def __init__(self, artifact_uri: str) -> None:
        self.artifact_uri = artifact_uri.rstrip("/")

    def write(
        self,
        frame: pl.DataFrame,
        *,
        name: str,
        version: str,
        storage_format: str,
        writer_options: Optional[Mapping[str, Any]] = None,
    ) -> str:
        pass

    def read(self, storage_path: str, storage_format: str) -> pl.DataFrame:
        pass

    def remove(self, storage_path: str) -> None:
        pass

    def exists(self, storage_path: str) -> bool:
        pass


class LocalArtifactBackend(ArtifactBackend):
    name = "local"

    def __init__(self, artifact_path: Path) -> None:
        self.base_path = artifact_path.expanduser().resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)
        super().__init__(str(self.base_path))

    def write(
        self,
        frame: pl.DataFrame,
        *,
        name: str,
        version: str,
        storage_format: str,
        writer_options: Optional[Mapping[str, Any]] = None,
    ) -> str:
        pass

    def read(self, storage_path: str, storage_format: str) -> pl.DataFrame:
        pass

    def remove(self, storage_path: str) -> None:
        pass

    def exists(self, storage_path: str) -> bool:
        pass


class PyArrowArtifactBackend(ArtifactBackend):
    name = "pyarrow"

    def __init__(self, artifact_uri: str) -> None:
        fs, base_path = pa_fs.FileSystem.from_uri(artifact_uri)
        if base_path:
            fs = pa_fs.SubTreeFileSystem(base_path, fs)
        self._fs = fs
        super().__init__(artifact_uri)
        self._clean_base = self.artifact_uri.rstrip("/")

    def write(
        self,
        frame: pl.DataFrame,
        *,
        name: str,
        version: str,
        storage_format: str,
        writer_options: Optional[Mapping[str, Any]] = None,
    ) -> str:
        pass

    def read(self, storage_path: str, storage_format: str) -> pl.DataFrame:
        pass

    def remove(self, storage_path: str) -> None:
        pass

    def exists(self, storage_path: str) -> bool:
        pass

    def _relative_path(self, storage_path: str) -> str:
        pass
class FeatureStore:
    """
    Lightweight on-disk feature store with metadata cataloguing.
    """

    def __init__(
        self,
        root_path: Optional[Union[str, os.PathLike[str]]] = None,
        catalog_filename: str = "catalog.json",
        default_storage_format: str = "parquet",
        artifact_uri: Optional[str] = None,
        artifact_backend: Optional[ArtifactBackend] = None,
        enable_locking: bool = True,
        lock_timeout: float = 30.0,
        lock_poll_interval: float = 0.2,
    ) -> None:
        _warn_feature_store_beta()
        self.root_path = _resolve_root_path(root_path)
        self.root_path.mkdir(parents=True, exist_ok=True)
        self.catalog_path = self.root_path / catalog_filename
        self.default_storage_format = default_storage_format
        self._registry: Dict[str, RegisteredTransform] = {}
        self._catalog: List[Dict[str, Any]] = self._load_catalog()
        artifact_uri = artifact_uri or str(self.root_path)
        self._artifact_backend = artifact_backend or _create_artifact_backend(artifact_uri)
        self.enable_locking = enable_locking
        self._lock_manager = (
            FileLockManager(
                self.root_path / ".locks",
                timeout=lock_timeout,
                poll_interval=lock_poll_interval,
            )
            if enable_locking
            else None
        )

    # ------------------------------------------------------------------ #
    # Registration
    # ------------------------------------------------------------------ #
    def register(
        self,
        name: str,
        transform: TransformCallable,
        *,
        default_kwargs: Optional[Mapping[str, Any]] = None,
        description: Optional[str] = None,
        tags: Optional[Iterable[str]] = None,
        default_key_columns: Optional[Sequence[str]] = None,
        extra_metadata: Optional[Mapping[str, Any]] = None,
    ) -> "FeatureStore":
        pass

    # ------------------------------------------------------------------ #
    # Build / Load
    # ------------------------------------------------------------------ #
    def build(
        self,
        name: str,
        data: Union[pd.DataFrame, pl.DataFrame],
        *,
        params: Optional[Mapping[str, Any]] = None,
        refresh: bool = False,
        version: Optional[str] = None,
        key_columns: Optional[Sequence[str]] = None,
        storage_format: Optional[str] = None,
        tags: Optional[Iterable[str]] = None,
        extra_metadata: Optional[Mapping[str, Any]] = None,
        return_engine: str = "auto",
        writer_options: Optional[Mapping[str, Any]] = None,
    ) -> FeatureSetResult:
        pass

    def load(
        self,
        name: str,
        *,
        version: Optional[str] = None,
        return_engine: str = "polars",
    ) -> FeatureSetResult:
        pass

    # ------------------------------------------------------------------ #
    # Catalog inspection
    # ------------------------------------------------------------------ #
    def list_feature_sets(self, name: Optional[str] = None) -> pd.DataFrame:
        pass

    def describe(self, name: str, version: Optional[str] = None) -> FeatureSetMetadata:
        pass

    def drop(self, name: str, version: Optional[str] = None, *, delete_artifact: bool = True) -> None:
        pass

    def assemble(
        self,
        feature_specs: Sequence[Union[str, Tuple[str, str]]],
        *,
        join_keys: Optional[Sequence[str]] = None,
        how: str = "left",
        return_engine: str = "polars",
    ) -> FeatureSetResult:
        pass

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _get_registered_transform(self, name: str) -> RegisteredTransform:
        pass

    def _find_entry(
        self,
        *,
        name: str,
        cache_key: Optional[str] = None,
        version: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        pass

    def _load_entry(
        self,
        entry: Mapping[str, Any],
        *,
        return_engine: str,
        from_cache: bool,
    ) -> FeatureSetResult:
        pass

    def _load_catalog(self) -> List[Dict[str, Any]]:
        pass

    def _persist_catalog(self) -> None:
        pass


class FeatureStoreAccessor:
    """
    Polars `.tk` accessor helper that operates against a feature store instance.
    """

    def __init__(
        self,
        frame: pl.DataFrame,
        *,
        store: Optional[FeatureStore] = None,
        store_kwargs: Optional[Mapping[str, Any]] = None,
    ) -> None:
        self._frame = frame
        if store is not None:
            self._store = store
        else:
            store_kwargs = dict(store_kwargs or {})
            self._store = FeatureStore(**store_kwargs)

    @property
    def store(self) -> FeatureStore:
        pass

    def register(self, *args: Any, **kwargs: Any) -> FeatureStore:
        pass

    def build(self, name: str, **kwargs: Any) -> FeatureSetResult:
        pass

    def load(self, *args: Any, **kwargs: Any) -> FeatureSetResult:
        pass

    def assemble(self, *args: Any, **kwargs: Any) -> FeatureSetResult:
        pass


def feature_store(
    root_path: Optional[Union[str, os.PathLike[str]]] = None,
    **kwargs: Any,
) -> FeatureStore:
    """
    Convenience factory mirroring the OO constructor.
    """
    pass


# ---------------------------------------------------------------------- #
# Helpers
# ---------------------------------------------------------------------- #

def _resolve_root_path(
    root_path: Optional[Union[str, os.PathLike[str]]],
) -> Path:
    pass


def _pytimetk_version() -> str:
    pass


def _package_versions() -> Dict[str, str]:
    pass


def _dataframe_fingerprint(data: Union[pd.DataFrame, pl.DataFrame]) -> str:
    pass


def _ensure_polars_df(data: Union[pd.DataFrame, pl.DataFrame]) -> pl.DataFrame:
    pass


def _read_frame(target: Union[Path, str, BinaryIO], storage_format: str) -> pl.DataFrame:
    pass


def _write_frame(
    frame: pl.DataFrame,
    target: Union[Path, str, BinaryIO],
    storage_format: str,
    writer_options: Optional[Mapping[str, Any]],
) -> None:
    pass


def _metadata_from_dict(entry: Mapping[str, Any]) -> FeatureSetMetadata:
    pass


def _resolve_return_engine(return_engine: str, base_input: Any = None) -> str:
    pass


def _coerce_return_frame(
    frame: pl.DataFrame,
    *,
    return_engine: str,
    base_input: Any = None,
) -> Union[pd.DataFrame, pl.DataFrame]:
    pass


def _normalise_for_hash(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    def serialise(value: Any) -> Any:
        pass
    pass


def _make_cache_key(name: str, data_fingerprint: str, transform_fingerprint: str) -> str:
    pass


def _derive_version(cache_key: str) -> str:
    pass


def _extension_for_format(storage_format: str) -> str:
    pass


def _create_artifact_backend(artifact_uri: str) -> ArtifactBackend:
    pass


def _create_artifact_backend_with_name(name: str, artifact_uri: str) -> ArtifactBackend:
    pass


def _backend_from_metadata(entry: Mapping[str, Any], default_backend: ArtifactBackend) -> ArtifactBackend:
    pass


def _join_uri(base: str, *segments: str) -> str:
    pass


def _parse_feature_spec(spec: Union[str, Tuple[str, str]]) -> Tuple[str, Optional[str]]:
    pass


def _json_serialize(obj: Any) -> Jsonable:
    pass

from __future__ import annotations

from typing import Callable, List, Optional, Sequence, Tuple, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from pytimetk.utils.parallel_helpers import conditional_tqdm

try:  # pragma: no cover - optional dependency
    import ray  # type: ignore
except ImportError:  # pragma: no cover - ray optional
    ray = None  # type: ignore


def ensure_ray_initialized(num_cpus: Optional[int] = None):
    """
    Initialize Ray on-demand and return the module.

    Parameters
    ----------
    num_cpus : Optional[int]
        Optional CPU limit to pass to ``ray.init``.
    """
    pass


def run_ray_tasks(
    func: Callable,
    args_list: Sequence[Tuple],
    *,
    num_cpus: Optional[int],
    desc: str,
    show_progress: bool,
) -> List:
    """
    Execute ``func`` across ``args_list`` using Ray.

    Parameters
    ----------
    func : Callable
        Function to execute remotely. Must be picklable.
    args_list : Sequence[Tuple]
        Positional arguments for each invocation.
    num_cpus : Optional[int]
        Desired CPU count for the Ray cluster. ``None`` lets Ray decide.
    desc : str
        Description for the progress iterator.
    show_progress : bool
        Whether to display progress via tqdm.
    """
    pass


__all__ = ["ensure_ray_initialized", "run_ray_tasks"]

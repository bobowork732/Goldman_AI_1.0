"""Execution scheduler for frame generation tasks."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


class FrameScheduler:
    """Runs frame work in a thread pool for better throughput."""

    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers

    def run(self, fn: Callable[[T], T], items: Iterable[T]) -> list[T]:
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(fn, items))

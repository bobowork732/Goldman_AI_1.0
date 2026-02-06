"""Simple multithreaded frame scheduler."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, TypeVar


T = TypeVar("T")
R = TypeVar("R")


class FrameScheduler:
    def __init__(self, workers: int = 4) -> None:
        self.workers = workers

    def run(self, items: Iterable[T], job: Callable[[T], R]) -> list[R]:
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            return list(executor.map(job, items))

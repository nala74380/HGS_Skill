from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, List

def run_parallel(actions: List[Callable], context: Any) -> List[Any]:
    """Execute a list of callables in parallel with the same context."""
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(action, context) for action in actions]
        for future in as_completed(futures):
            results.append(future.result())
    return results
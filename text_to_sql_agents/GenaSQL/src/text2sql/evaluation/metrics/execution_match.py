"""Execution match metric for evaluating Text-to-SQL models,
based on the execution results as list of Python dictionaries.

More about the metric can be found on the paper for the BIRD Text-to-SQL benchmark paper.
https://arxiv.org/pdf/2305.03111

This implementation differs from the benchmark's in that it takes a list of dictionaries not tuples.
In edge where the database result has two columns with the same name,
information will be lost since dictionaries and json object can't hold them all.
"""

import math
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class ComparableTuple:
    """A tuple wrapper that handles float comparison with tolerance.

    Supports comparison of mixed-type tuples where float values are compared
    with relative tolerance of 1e-9.
    """

    data: tuple

    def __eq__(self, other):
        if len(self.data) != len(other.data):
            return False

        for v1, v2 in zip(self.data, other.data):
            if isinstance(v1, float) and isinstance(v2, float):
                # Whole point of this clase is so that we can do set comparison
                # while handling floating-point representation errors
                if not math.isclose(v1, v2, rel_tol=1e-9):
                    return False
            elif v1 != v2:
                return False
        return True

    def __hash__(self):
        # Convert floats to strings with limited precision for hashing
        processed = tuple(f"{x:.8f}" if isinstance(x, float) else x for x in self.data)
        return hash(processed)


def execution_match(
    prediction: List[Dict[str, Any]],
    ground_truth: List[Dict[str, Any]],
) -> bool:
    """Compare two lists of dictionaries for equality, handling float values."""

    def transform_results(ex_result):
        new_ex_result = []
        for row in ex_result:
            new_row = ComparableTuple(tuple(row.values()))
            new_ex_result.append(new_row)
        return set(new_ex_result)

    return transform_results(ground_truth) == transform_results(prediction)
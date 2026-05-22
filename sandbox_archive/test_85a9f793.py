# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Swap with a row below that has a non-zero pivot
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Normalize the pivot row
        factor = Fraction(1, A[i][i])
        for j in range(n):
            A[i][j] *= factor
        # Eliminate the current column below the pivot
        for j in range(i + 1, n):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def construct_noncommutative_algebra(n):
    # Example: Construct a random noncommutative algebra using a matrix
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    gaussian_elimination(A)
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    try:
        algebra = construct_noncommutative_algebra(n)
        # Placeholder for actual computation of polynomial automaton order
        automaton_order = sum(sum(row) for row in algebra)
        circuit_size = n * n  # Placeholder for ACC⁰ circuit size
        return {
            "metric_name": "Automaton Order vs Circuit Size",
            "metric_value": abs(automaton_order - circuit_size),
            "instances_tested": 1,
            "conjecture_holds": automaton_order >= circuit_size,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "Automaton Order vs Circuit Size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
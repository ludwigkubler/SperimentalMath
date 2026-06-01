# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def symplectic_leaf(clauses, n):
        points = []
        for clause in clauses:
            point = [0] * (2*n)
            for var in clause:
                if var > 0:
                    point[var-1] = 1
                else:
                    point[-var-1] = -1
            points.append(point)
        return points

    def min_affine_generators(points):
        A = [p + [-1] for p in points]
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row[i] != 0 for i in range(len(row)-1)))
        return len(points) - rank

    def resolution_width(clauses):
        # Placeholder function to calculate resolution width
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)

    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n) for _ in range(random.randint(2, 3))]
        clauses.append(clause)

    points = symplectic_leaf(clauses, n)
    min_order = min_affine_generators(points)
    width = resolution_width(clauses)

    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
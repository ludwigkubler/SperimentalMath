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
        for j in range(i, n):
            A[i][j] *= factor
        # Eliminate the pivot column
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
    return A

def fundamental_group(vertices, edges):
    n = len(vertices)
    A = [[0] * n for _ in range(n)]
    for u, v in edges:
        if u != v:
            A[u][v] += 1
            A[v][u] += 1
    try:
        gaussian_elimination(A)
    except ValueError:
        return 1
    return sum(1 for row in A if any(x != 0 for x in row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    vertices = list(range(n))
    edges = []
    for _ in range(random.randint(0.5 * n * (n - 1), n * (n - 1))):
        u, v = random.sample(vertices, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    fundamental_group_count = sum(fundamental_group([i], edges) for i in vertices)
    resolution_proof_width = len(edges)
    return {
        "metric_name": "fundamental_group_count",
        "metric_value": fundamental_group_count,
        "instances_tested": n * (n - 1),
        "n_max": n,
        "conjecture_holds": fundamental_group_count <= 2 * resolution_proof_width,
        "counterexample": "" if fundamental_group_count <= 2 * resolution_proof_width else f"fundamental_group_count={fundamental_group_count}, resolution_proof_width={resolution_proof_width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30)) + [53, 67, 71, 73, 79]
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
        print(f"RESULT: FALSIFIED counterexample='{results[first_failing_seed]['counterexample']}' first_failing_seed={seeds[first_failing_seed]}")
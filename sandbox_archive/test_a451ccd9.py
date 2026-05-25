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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = -1
            for i in range(rank, m):
                if A[i][j] != 0:
                    i_max = i
                    break
            if i_max == -1:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    factor = Fraction(A[i][j], A[rank][j])
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
        return rank

    def sos_degree(poly):
        # Placeholder function to determine SOS degree
        # This is a dummy implementation and should be replaced with actual logic
        return len(poly)

    def max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges

    def moment_matrix(edges, n):
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            M[0][i] = M[i][0] = Fraction(1)
        for u, v in edges:
            M[u+1][v+1] += Fraction(1)
            M[v+1][u+1] += Fraction(1)
        return M

    def max_cut_ratio(poly, edges):
        # Placeholder function to compute max-cut ratio
        # This is a dummy implementation and should be replaced with actual logic
        return 0.879

    n = random.choice([5, 10, 15, 20, 30, 40])
    edges = max_cut_instance(n)
    M = moment_matrix(edges, n)
    rank = gaussian_elimination(M)
    d = sos_degree(poly) if 'poly' in locals() else None
    ratio = max_cut_ratio(poly, edges) if 'poly' in locals() else None

    return {
        "metric_name": "Rank of Moment Matrix",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= d and ratio > 0.878 if d is not None else False,
        "counterexample": "mapping_undefined" if d is None else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")
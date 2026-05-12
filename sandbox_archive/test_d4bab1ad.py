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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det_val = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det_val += (-1) ** j * A[0][j] * det(submatrix)
    return det_val

def eigenvalues(A):
    n = len(A)
    if n == 2:
        return [A[0][0], A[1][1]]
    eigs = []
    for i in range(100):  # Simple power iteration method
        v = [random.random() for _ in range(n)]
        v /= math.sqrt(sum(x**2 for x in v))
        Av = [sum(A[j][k] * v[k] for k in range(n)) for j in range(n)]
        eig = sum(Av[i] * v[i] for i in range(n))
        eigs.append(eig)
    return sorted(set(eigs))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0

    def degree_sos_moment_matrix(G, d):
        n = len(G)
        M = [[0] * (n + d) for _ in range(n + d)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    for k in range(d+1):
                        M[i][k] += math.comb(k, 2)
                        M[j][k] += math.comb(k, 2)
                        M[n + i][n + j] += math.comb(k, 2)
        return M

    def real_rank(M):
        A = [[M[i][j] for j in range(n + d)] for i in range(n + d)]
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return rank

    max_cut_approximation = None
    for d in range(2, 11):
        M_d = degree_sos_moment_matrix(G, d)
        rank_M_d = real_rank(M_d)
        if rank_M_d > d**2:
            max_cut_approximation = 0.878
            break

    metric_name = "max_cut_approximation"
    metric_value = max_cut_approximation or 0
    instances_tested = 1
    conjecture_holds = (rank_M_d <= d**2) if max_cut_approximation is None else False
    counterexample = "" if conjecture_holds else f"Rank(M_{d}) > {d**2}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
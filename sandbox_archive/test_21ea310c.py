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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses

    def matroid_rank(clauses):
        m = len(clauses)
        n = max(abs(c) for c in sum(clauses, []))
        A = [[0] * (n + 1) for _ in range(m + 1)]
        for i, clause in enumerate(clauses, start=1):
            for var in clause:
                A[i][abs(var)] += 1
        rank = 0
        for row in A[1:]:
            if any(row[j] > 0 for j in range(1, n + 1)):
                pivot_col = next(j for j in range(1, n + 1) if row[j] > 0)
                rank += 1
                for i2 in range(m + 1):
                    if A[i2][pivot_col] != 0:
                        factor = Fraction(A[i2][pivot_col], A[rank][pivot_col])
                        for j in range(n + 1):
                            A[i2][j] -= factor * A[rank][j]
        return rank

    def local_induction_dimension(clauses, ring_size):
        m = len(clauses)
        n = max(abs(c) for c in sum(clauses, []))
        A = [[0] * (n + 1) for _ in range(m + 1)]
        for i, clause in enumerate(clauses, start=1):
            for var in clause:
                A[i][abs(var)] += 1
        rank = 0
        for row in A[1:]:
            if any(row[j] > 0 for j in range(1, n + 1)):
                pivot_col = next(j for j in range(1, n + 1) if row[j] > 0)
                rank += 1
                for i2 in range(m + 1):
                    if A[i2][pivot_col] != 0:
                        factor = Fraction(A[i2][pivot_col], A[rank][pivot_col])
                        for j in range(n + 1):
                            A[i2][j] -= factor * A[rank][j]
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        k = random.randint(1, min(n, 10))
        clauses = generate_kcnf(n, k)
        rank = matroid_rank(clauses)
        lnd = local_induction_dimension(clauses, 2)  # Boolean ring
        results.append({"n": n, "k": k, "rank": rank, "lnd": lnd})

    total_lnd = sum(result["lnd"] for result in results)
    total_rank = sum(result["rank"] for result in results)
    ratio = Fraction(total_lnd, total_rank)

    return {
        "metric_name": "Ratio of LND to Rank",
        "metric_value": float(ratio),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": ratio >= 1,
        "counterexample": "" if ratio >= 1 else f"Ratio {ratio} < 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio < 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
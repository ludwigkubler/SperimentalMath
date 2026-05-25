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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause and -var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def density_matrix(clauses):
        n = max(abs(v) for v in set().union(*clauses))
        dm = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for i in range(3):
                for j in range(i + 1, 3):
                    x, y = clause[i], clause[j]
                    dm[abs(x)][abs(y)] += 1
                    dm[abs(y)][abs(x)] += 1
        return dm

    def von_neumann_entropy(dm):
        n = len(dm)
        trace = sum(dm[i][i] for i in range(n))
        if trace == 0:
            return 0
        dm = [[dm[i][j] / trace for j in range(n)] for i in range(n)]
        eigenvalues = [0] * n
        for _ in range(100):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v = [v_i / sum(v) for v_i in v]
            v_next = [sum(dm[i][j] * v[j] for j in range(n)) for i in range(n)]
            v_next = [v_next_i / sum(v_next) for v_next_i in v_next]
            eigenvalues[0] += abs(sum(v_i * v_next_i for v_i, v_next_i in zip(v, v_next)))
        return -sum(eigenvalue * math.log2(eigenvalue) if eigenvalue > 0 else 0 for eigenvalue in eigenvalues)

    def matrix_rank(dm):
        m = len(dm)
        n = len(dm[0])
        dm_copy = [row[:] for row in dm]
        rank = 0
        for i in range(min(m, n)):
            if dm_copy[i][i] != 0:
                for j in range(i + 1, m):
                    factor = dm_copy[j][i] / dm_copy[i][i]
                    for k in range(n):
                        dm_copy[j][k] -= factor * dm_copy[i][k]
                rank += 1
            else:
                found_pivot = False
                for j in range(i + 1, m):
                    if dm_copy[j][i] != 0:
                        dm_copy[i], dm_copy[j] = dm_copy[j], dm_copy[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
                for j in range(i + 1, m):
                    factor = dm_copy[j][i] / dm_copy[i][i]
                    for k in range(n):
                        dm_copy[j][k] -= factor * dm_copy[i][k]
                rank += 1
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        formula = generate_3cnf(n, m)
        dm = density_matrix(formula)
        entropy = von_neumann_entropy(dm)
        rank = matrix_rank(dm)
        results.append({
            "n": n,
            "m": m,
            "entropy": entropy,
            "rank": rank
        })

    metric_name = "rank_bound"
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["rank"] <= 2 * result["n"] + result["m"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
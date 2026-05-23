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
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def min_rank(A):
        rank = 0
        m, n = len(A), len(A[0])
        for i in range(m):
            if any(A[i][j] != 0 for j in range(n)):
                rank += 1
        return rank

    def generate_cnf(n):
        clauses = []
        for _ in range(2 ** (n - 1)):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)]
            for j in range(1, n):
                if random.choice([True, False]):
                    clause.append(random.randint(1, n) * (-1 if random.choice([True, False]) else 1))
            clauses.append(clause)
        return clauses

    def etale_cohomology(cnf):
        m = len(cnf)
        A = [[0] * (m + 1) for _ in range(m)]
        for i in range(m):
            for j in range(m):
                if cnf[i][j] != 0:
                    A[i][j] = 1
        return gaussian_elimination(A)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        cohomology = etale_cohomology(cnf)
        rank = min_rank(cohomology)
        results.append((n, rank))
    
    if not results:
        return {
            "metric_name": "Minimal Rank of Etale Cohomology Groups",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_rank = sum(rank for _, rank in results)
    mean_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((rank - mean_rank) ** 2 for _, rank in results) / len(results))
    
    C = max(1, max_rank)
    k = 1
    
    conjecture_holds = all(rank ** n <= C * n ** k for n, rank in results)
    counterexample = "" if conjecture_holds else "n={}, rank={}".format(n_values[results.index(max(results, key=lambda x: x[1]))], max_rank)
    
    return {
        "metric_name": "Minimal Rank of Etale Cohomology Groups",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_rank, std_rank, support_fraction))
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[seeds.index(first_failing_seed)]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
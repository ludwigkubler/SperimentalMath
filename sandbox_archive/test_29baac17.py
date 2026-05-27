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
        n = len(A)
        for i in range(n):
            pivot_row = max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[pivot_row] = A[pivot_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                return float('inf')  # Indeterminate rank
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = -A[k][i]
                    for j in range(n):
                        A[k][j] += factor * A[i][j]
        return sum(1 for row in A if any(row))

    def minimal_rank_of_quadratic_form(clauses):
        n = len(clauses)
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                Q[i][j] = sum(1 for clause in clauses if (i + 1) in clause and (j + 1) in clause)
                Q[j][i] = Q[i][j]
        return gaussian_elimination(Q)

    def generate_sat_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses

    resolution_refutation_sizes = [random.randint(50, 200) for _ in range(30)]
    ranks = []

    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        for refutation_size in resolution_refutation_sizes:
            clauses = generate_sat_instance(n)
            rank = minimal_rank_of_quadratic_form(clauses)
            if rank != float('inf'):
                ranks.append(rank)
                instances_tested += 1

    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    
    correlation_coefficient = sum((ranks[i] - mean_rank) * (resolution_refutation_sizes[i] - mean(resolution_refutation_sizes)) for i in range(len(ranks))) / (len(ranks) * std_rank * math.sqrt(sum((x - mean(resolution_refutation_sizes)) ** 2 for x in resolution_refutation_sizes)))
    
    conjecture_holds = correlation_coefficient <= -0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient > -0.7"
    
    return {
        "metric_name": "MinimalRankOfQuadraticForms",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
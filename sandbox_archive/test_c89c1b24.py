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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if -var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def p_adic_representation(clauses):
        n = max(abs(v) for clause in clauses for v in clause)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for i, var in enumerate(clause):
                for j in range(i + 1, len(clause)):
                    matrix[abs(var)][abs(clause[j])] += 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        for i in range(m):
            if all(matrix[i][j] == 0 for j in range(n)):
                continue
            pivot_col = next(j for j in range(n) if matrix[i][j] != 0)
            for j in range(i + 1, m):
                factor = -matrix[j][pivot_col] / matrix[i][pivot_col]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row[j] != 0 for j in range(n)))
        return rank
    
    def n_half_k_fourth(n, k):
        return math.sqrt(n) * (k ** 0.25)
    
    results = []
    for _ in range(30):  # Ensure at least 24 instances per seed
        n = random.randint(5, 40)
        k = random.randint(3, 10)
        clauses = generate_kcnf(n, k)
        matrix = p_adic_representation(clauses)
        rank_value = rank(matrix)
        expected_rank = n_half_k_fourth(n, k)
        results.append({
            "metric_name": "Rank",
            "metric_value": rank_value,
            "instances_tested": 1,
            "conjecture_holds": abs(rank_value - expected_rank) <= 0.2 * expected_rank,
            "counterexample": "" if abs(rank_value - expected_rank) <= 0.2 * expected_rank else f"n={n}, k={k}"
        })
    
    return {
        "seed": seed,
        "metric_name": "Average Rank",
        "metric_value": sum(result["metric_value"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if result["counterexample"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
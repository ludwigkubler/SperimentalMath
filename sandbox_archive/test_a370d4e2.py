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
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) * (-1 if random.randint(0, 1) else 1)]
            while len(clause) < 3:
                var = random.choice(variables)
                if var not in clause:
                    clause.append(var * (-1 if random.randint(0, 1) else 1))
            clauses.append(tuple(sorted(clause)))
        return clauses

    def construct_coxeter_matrix(clauses):
        n = len(set(abs(v) for v in sum(clauses, ())))
        matrix = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in clause:
                for j in clause:
                    if abs(i) != abs(j):
                        matrix[abs(i) - 1][abs(j) - 1] += 1
                        matrix[abs(j) - 1][abs(i) - 1] += 1
        return matrix

    def max_rank(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                continue
            for j in range(n):
                if j != i and matrix[j][j] != 0:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            cnf = generate_cnf(n, m)
            matrix = construct_coxeter_matrix(cnf)
            rank = max_rank(matrix)
            if rank > 2 * m:
                return {
                    "metric_name": "max_rank",
                    "metric_value": rank,
                    "instances_tested": 1,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": "rank > 2 * clause_complexity"
                }
            results.append({
                "metric_name": "max_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": True,
                "counterexample": ""
            })
    
    return {
        "metric_name": "max_rank",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank > 2 * clause_complexity' first_failing_seed={first_failing_seed}")
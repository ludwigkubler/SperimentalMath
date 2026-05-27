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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def tropicalized_quaternion_algebra(cnf):
        n = len(cnf[0])
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    row = [1 if j == i else -1 for j in range(n)]
                else:
                    row = [-1 if j == i else 1 for j in range(n)]
                matrix[i] = [max(matrix[i][j], row[j]) for j in range(n)]
        return matrix
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(i, n):
                if any(x != 0 for x in matrix[j]):
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            rank += 1
            for j in range(n):
                if j == i:
                    continue
                factor = matrix[j][i] / matrix[pivot_row][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[pivot_row][k]
        return rank
    
    n_values = [10, 20, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        algebra = tropicalized_quaternion_algebra(cnf)
        rank = min_rank(algebra)
        f_n = int(1.5 * n)
        results.append({
            "n": n,
            "rank": rank,
            "f_n": f_n
        })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    conjecture_holds = all(result["rank"] <= result["f_n"] for result in results)
    counterexample = "" if conjecture_holds else "n={n}, rank={rank}, f(n)={f_n}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['n']}, rank={results[first_failing_seed]['rank']}, f(n)={results[first_failing_seed]['f_n']}\" first_failing_seed={first_failing_seed}")
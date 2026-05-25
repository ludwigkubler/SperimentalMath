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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Make all entries below pivot zero
        pivot = A[i][i]
        for k in range(i+1, n):
            factor = -A[k][i] / pivot
            for j in range(n):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += factor * A[i][j]

def min_rank(A):
    gaussian_elimination(A)
    rank = sum(1 for row in A if any(row))
    return rank

def p_adic_diff(clause, n):
    diff = [0] * (n + 1)
    for var in clause:
        diff[var] += 1
        diff[-var] -= 1
    return diff

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    total_rank = 0
    
    for _ in range(instances_tested):
        # Generate a random CNF formula with n variables and clauses of length up to n
        num_clauses = random.randint(n // 2, n)
        cnf_formula = []
        for _ in range(num_clauses):
            clause_length = random.randint(1, n)
            clause = [random.choice([-i, i]) for i in range(1, n + 1) if random.random() < clause_length / n]
            cnf_formula.append(clause)
        
        # Compute the p-adic differential form of the CNF formula
        p_adic_diffs = []
        for clause in cnf_formula:
            diff = p_adic_diff(clause, n)
            p_adic_diffs.extend(diff)
        
        # Determine the minimal rank of the p-adic differential forms
        rank = min_rank([p_adic_diffs[i:i+n+1] for i in range(0, len(p_adic_diffs), n + 1)])
        total_rank += rank
    
    metric_value = total_rank / instances_tested
    conjecture_holds = (metric_value <= 1.5 * math.sqrt(n)) and (metric_value >= 0.5 * math.sqrt(n))
    counterexample = "" if conjecture_holds else f"n={n}, rank={metric_value}"
    
    return {
        "metric_name": "Minimal Rank of p-Adic Differentials",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={res['instances_tested']}, rank={res['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
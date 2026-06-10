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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        rref = gaussian_elimination(A)
        return sum(1 for row in rref if any(row))

    def p_adic_valuation(a, p):
        if a == 0:
            return float('inf')
        count = 0
        while a % p == 0:
            a //= p
            count += 1
        return count

    def rank_variance(A):
        m, n = len(A), len(A[0])
        mean = sum(sum(row) for row in A) / (m * n)
        variance = sum((sum(row) - mean) ** 2 for row in A) / (m * n)
        return variance

    def generate_instance(n):
        A = [[random.randint(0, 100) for _ in range(n)] for _ in range(n)]
        return A

    instances_tested = 30
    n_max = 40
    p = 2  # Example prime number for p-adic valuation
    
    rank_p_val = []
    rank_var = []

    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        A = generate_instance(n)
        r_p_val = sum(p_adic_valuation(a, p) for row in A for a in row)
        r_var = rank_variance(A)
        
        rank_p_val.append(r_p_val)
        rank_var.append(r_var)

    correlation_coefficient = sum((rank_p_val[i] - sum(rank_p_val) / instances_tested) * (rank_var[i] - sum(rank_var) / instances_tested) for i in range(instances_tested)) / ((instances_tested - 1) * math.sqrt(sum((rank_p_val[i] - sum(rank_p_val) / instances_tested) ** 2 for i in range(instances_tested))) * math.sqrt(sum((rank_var[i] - sum(rank_var) / instances_tested) ** 2 for i in range(instances_tested))))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
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
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence support_fraction={support_fraction}")
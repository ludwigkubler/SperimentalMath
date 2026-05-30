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

def generate_k_cnf(n, k):
    clauses = []
    for _ in range(k * n):
        clause = set()
        while len(clause) < 2:
            lit = random.randint(1, n)
            if random.choice([True, False]):
                lit = -lit
            clause.add(lit)
        clauses.append(tuple(sorted(clause)))
    return clauses

def cc_r(k_cnf):
    n = len(set(abs(lit) for clause in k_cnf for lit in clause))
    m = len(k_cnf)
    if n == 1:
        return 0
    return math.ceil(math.log2(m * (n - 1)))

def minimal_tropical_motivic_rank(k_cnf):
    rank = 0
    for clause in k_cnf:
        rank += max(abs(lit) for lit in clause)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k_cnf = generate_k_cnf(n, n // 2)
        m_trop = minimal_tropical_motivic_rank(k_cnf)
        cc_r_val = cc_r(k_cnf)
        
        if abs(m_trop) > 10:
            return {
                "metric_name": "Pearson Correlation Coefficient",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"m_trop({m_trop}) > 10"
            }
        
        results.append((abs(m_trop), cc_r_val ** 0.5))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Insufficient instances tested ({len(results)})"
        }
    
    n = len(results)
    x_sum, y_sum = sum(x for x, _ in results), sum(y for _, y in results)
    xy_sum = sum(x * y for x, y in results)
    x2_sum = sum(x ** 2 for x, _ in results)
    y2_sum = sum(y ** 2 for _, y in results)
    
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * x2_sum - x_sum ** 2) * (n * y2_sum - y_sum ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Denominator is zero"
        }
    
    correlation_coefficient = numerator / denominator
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    if any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m_trop > 10\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
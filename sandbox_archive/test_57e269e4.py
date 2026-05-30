# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = [random.randint(1, 2*n) if random.choice([True, False]) else -random.randint(1, 2*n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def communication_complexity(cnf):
        # Simplified simulation of two-party communication complexity
        n = len(cnf[0])
        return n * len(cnf)
    
    def tropical_motivic_rank(cnf):
        # Simplified computation of minimal tropical motivic rank
        n = len(cnf[0])
        rank = 0
        for clause in cnf:
            rank += sum(1 for lit in clause if abs(lit) <= n)
        return rank
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = (sum((xi - mean_x)**2 for xi in x) / len(x))**0.5
        std_y = (sum((yi - mean_y)**2 for yi in y) / len(y))**0.5
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_trop_values = []
    cc_r_values = []
    
    for n in n_values:
        cnf = generate_k_cnf(n, k=3)
        m_trop = tropical_motivic_rank(cnf)
        cc_r = communication_complexity(cnf)
        m_trop_values.append(abs(m_trop))
        cc_r_values.append(cc_r**0.5)
    
    correlation_coefficient = pearson_correlation(m_trop_values, cc_r_values)
    conjecture_holds = correlation_coefficient >= 0.8 and max(m_trop_values) <= 10
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
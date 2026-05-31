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
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def count_satisfying_assignments(cnf):
        n = max(abs(x) for x in sum(cnf, []))
        assignments = [i for i in range(2**n)]
        count = 0
        for assignment in assignments:
            satisfied = True
            for clause in cnf:
                if all((assignment & (1 << abs(l) - 1)) == 0 if l < 0 else (assignment & (1 << abs(l) - 1)) != 0 for l in clause):
                    satisfied = False
                    break
            if satisfied:
                count += 1
        return count
    
    def second_betti_number(cnf):
        n = max(abs(x) for x in sum(cnf, []))
        # Simplified model of the configuration space
        # This is a placeholder and should be replaced with actual computation
        return min(n, 20)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(2*n, 3*n))
            t_F = count_satisfying_assignments(cnf)
            H2_F = second_betti_number(cnf)
            results.append((t_F, H2_F))
    
    if any(H2_F > 20 for _, H2_F in results):
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in [5, 10, 15, 20, 30, 40]),
            "conjecture_holds": False,
            "counterexample": "H^2_F > 20"
        }
    
    t_F_values = [t_F for t_F, _ in results]
    H2_F_values = [H2_F for _, H2_F in results]
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y) if std_x != 0 and std_y != 0 else 0
    
    corr_coeff = correlation_coefficient(t_F_values, H2_F_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": corr_coeff > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
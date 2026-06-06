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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([1, -1]) * i for i in range(1, n+1)]
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        depth = 0
        stack = []
        for clause in cnf:
            if all(x > 0 for x in clause):
                depth += 1
                stack.append(depth)
            else:
                depth -= 1
                stack.pop()
        return max(stack) if stack else 0
    
    def monomial_representation(cnf):
        n = len(cnf[0])
        monomials = []
        for i in range(2**n):
            monomial = [int(x) for x in format(i, f'0{n}b')]
            if all(monomial[j] * cnf[j][i//2**j] >= 0 for j in range(n)):
                monomials.append(monomial)
        return monomials
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        depth = frege_proof_depth(cnf)
        if depth == 0:
            continue
        monomials = monomial_representation(cnf)
        results.append((len(monomials), math.log(depth)))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    metric_value = pearson_correlation([x for x, _ in results], [y for _, y in results])
    conjecture_holds = metric_value > 0.5
    counterexample = "" if conjecture_holds else f"Metric value: {metric_value}"
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(result["metric_value"] <= 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] <= 0.5)
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation ≤ 0.5' first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
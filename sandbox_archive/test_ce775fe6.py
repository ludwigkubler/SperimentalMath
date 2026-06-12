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
    
    def generate_k_sat_instance(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def incidence_algebra(clauses):
        n = len(clauses[0])
        algebra = [[0] * (2 ** n) for _ in range(2 ** n)]
        for clause in clauses:
            mask = 0
            for var in clause:
                mask |= (1 << (var - 1))
            algebra[mask][mask] += 1
        return algebra
    
    def p_adic_metric_complexity(algebra, base):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value) / math.log2(base)
    
    def clause_tree_width(clauses):
        # Simplified estimation of clause tree width
        return len(clauses)
    
    base = 5  # Fixed base field K for p-adic metric complexity
    n_max = 40
    instances_tested = 30
    
    results = []
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        k = random.randint(n // 2, min(n * (n - 1) // 2, 40))
        clauses = generate_k_sat_instance(n, k)
        algebra = incidence_algebra(clauses)
        ctw = clause_tree_width(clauses)
        p_adic_complexity = p_adic_metric_complexity(algebra, base)
        
        results.append({
            "n": n,
            "k": k,
            "ctw": ctw,
            "p_adic_complexity": p_adic_complexity
        })
    
    correlation_coefficient = 0.0
    for result in results:
        correlation_coefficient += (result["ctw"] - sum(r["ctw"] for r in results) / instances_tested) * \
                                   (result["p_adic_complexity"] - sum(r["p_adic_complexity"] for r in results) / instances_tested)
    correlation_coefficient /= instances_tested
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient_too_low"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
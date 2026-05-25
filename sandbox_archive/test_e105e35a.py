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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def clause_indicator_polynomial(instance):
        n = len(instance) // 2
        polynomial = []
        for i in range(n):
            term = instance[i] * instance[n + i]
            polynomial.append(term)
        return polynomial
    
    def twisted_quotient_algebra(polynomial):
        n = len(polynomial)
        algebra = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    algebra[i][j] = 1
                else:
                    algebra[i][j] = polynomial[i] + polynomial[j]
        return algebra
    
    def min_rank(algebra):
        n = len(algebra)
        rank = 0
        for row in algebra:
            if any(row):
                rank += 1
        return rank
    
    def dpll_proof_length(instance):
        n = len(instance) // 2
        length = 0
        for i in range(n):
            if instance[i] == 1 and instance[n + i] == 0:
                length += 1
            elif instance[i] == 0 and instance[n + i] == 1:
                length += 1
        return length
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rho = 0
        total_l = 0
        
        for _ in range(30):
            instance = generate_instance(n)
            polynomial = clause_indicator_polynomial(instance)
            algebra = twisted_quotient_algebra(polynomial)
            rho = min_rank(algebra)
            l = dpll_proof_length(instance)
            
            instances_tested += 1
            total_rho += rho
            total_l += l
        
        avg_rho = total_rho / instances_tested
        avg_l = total_l / instances_tested
        correlation = (instances_tested * sum(rho * l for rho, l in zip(results, results)) - 
                       sum(results) * sum(results)) / math.sqrt((instances_tested * sum(rho**2 for rho in results) - sum(results)**2) *
                                                            (instances_tested * sum(l**2 for l in results) - sum(results)**2))
        
        results.append(correlation)
    
    metric_name = "Spearman's rank correlation"
    metric_value = sum(results) / len(results)
    conjecture_holds = all(r > 0.7 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
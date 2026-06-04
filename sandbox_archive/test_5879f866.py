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
    
    def compute_barcode_matrix(instance):
        n = len(instance)
        B = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n + 1):
                if instance[i] != instance[j]:
                    B[i][j] = 1
        return B
    
    def compute_betti_numbers(B):
        n = len(B) - 1
        H = [B]
        for i in range(1, n + 1):
            H.append([row[1:] for row in H[-1]])
        betti_0 = sum(1 for row in H[0] if sum(row) == 1)
        betti_1 = sum(1 for row in H[1] if sum(row) == 2 and all(row[j] != row[j + 1] for j in range(len(row) - 1)))
        return betti_0, betti_1
    
    def compute_resolution_width(instance):
        n = len(instance)
        clauses = [i for i, x in enumerate(instance) if x == 1]
        variables = set(range(n))
        width = 0
        while variables:
            new_variables = set()
            for clause in clauses:
                if all(var not in variables for var in range(n)):
                    continue
                new_var = random.choice([var for var in range(n) if var in variables and any(instance[var] == 1)])
                new_variables.add(new_var)
                width += 1
            variables -= new_variables
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_betti_sum = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):
            instance = generate_instance(n)
            B = compute_barcode_matrix(instance)
            betti_0, betti_1 = compute_betti_numbers(B)
            width = compute_resolution_width(instance)
            
            instances_tested += 1
            total_betti_sum += betti_0 + betti_1
            total_width += width
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_betti_sum = total_betti_sum / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * mean_betti_sum * mean_width - 
                               sum(betti_sum * width for betti_sum, width in zip([betti_0 + betti_1 for _ in range(instances_tested)], [width for _ in range(instances_tested)]))) / \
                              math.sqrt((instances_tested * sum(betti_sum**2 for betti_sum in [betti_0 + betti_1 for _ in range(instances_tested)]) - 
                                          (sum(betti_sum for betti_sum in [betti_0 + betti_1 for _ in range(instances_tested)]))**2) * 
                                        (instances_tested * sum(width**2 for width in [width for _ in range(instances_tested)]) - 
                                         (sum(width for width in [width for _ in range(instances_tested)]))**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_budget_exceeded")
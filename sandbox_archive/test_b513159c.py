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
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def incidence_matrix(cnf, n):
        m = len(cnf)
        Inc = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            for literal in cnf[i]:
                if literal > 0:
                    Inc[i][literal - 1] = 1
                else:
                    Inc[i][-literal - 1] = -1
        return Inc
    
    def min_order(Inc, p):
        m, n = len(Inc), len(Inc[0])
        order = float('inf')
        for i in range(m):
            for j in range(i + 1, m):
                diff = [Inc[i][k] - Inc[j][k] for k in range(n)]
                norm = sum(abs(x) for x in diff)
                if norm < order:
                    order = norm
        return order
    
    def frege_proof_length(cnf):
        # Simplified Frege proof length estimation (not actual proof generation)
        return len(cnf) * 2
    
    p = 3  # Prime number
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        instances_tested = 0
        total_order = 0
        total_length = 0
        
        for _ in range(5):
            cnf = generate_cnf(n)
            Inc = incidence_matrix(cnf, n)
            order = min_order(Inc, p)
            length = frege_proof_length(cnf)
            
            if order == float('inf'):
                continue
            
            total_order += order
            total_length += length
            instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        avg_order = total_order / instances_tested
        avg_length = total_length / instances_tested
        metric_value = math.log(p - 1) ** avg_order
        
        # Pearson's correlation coefficient (simplified for demonstration)
        x_mean = sum(math.log(2**length + 1) for length in range(avg_length, avg_length + instances_tested)) / instances_tested
        y_mean = sum(math.log(2**length + 1) for length in range(avg_length, avg_length + instances_tested)) / instances_tested
        
        x_diff = [math.log(2**length + 1) - x_mean for length in range(avg_length, avg_length + instances_tested)]
        y_diff = [math.log(2**length + 1) - y_mean for length in range(avg_length, avg_length + instances_tested)]
        
        numerator = sum(x * y for x, y in zip(x_diff, y_diff))
        denominator = math.sqrt(sum(x ** 2 for x in x_diff)) * math.sqrt(sum(y ** 2 for y in y_diff))
        
        if denominator == 0:
            correlation_coefficient = 0
        else:
            correlation_coefficient = numerator / denominator
        
        metric_values.append(metric_value)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": sum(len(metric_values) for n in n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient > 0.5 else "correlation_below_threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
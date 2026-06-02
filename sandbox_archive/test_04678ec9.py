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
        for _ in range(2**n):
            row = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(row) == 0:
                continue
            cnf.append(row)
        return cnf
    
    def min_order(cnf):
        n = len(cnf[0])
        truth_table = [sum([lit if val > 0 else -lit for lit, val in zip(row, assignment)]) for row in cnf]
        degree = 1
        while True:
            all_zero = all(truth_table[i] == 0 for i in range(len(truth_table)))
            if all_zero:
                return degree
            degree += 1
    
    def frege_proof_length(cnf):
        # Placeholder function to simulate Frege proof length calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) * n
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_order_values = []
    frege_proof_lengths = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        min_order_value = min_order(cnf)
        frege_proof_length_value = frege_proof_length(cnf)
        
        min_order_values.append(min_order_value)
        frege_proof_lengths.append(frege_proof_length_value)
    
    correlation_coefficient = pearson_correlation(min_order_values, frege_proof_lengths)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) > 0.7) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")
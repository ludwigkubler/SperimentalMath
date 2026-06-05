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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_matroid(M):
        rank = len(set(tuple(sorted(subset)) for subset in M if all(M[i] == 1 for i in subset)))
        return rank
    
    def compute_alexander_defect(M):
        n = len(M)
        matroid_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if all(M[i] == M[j] for k in range(2**n)):
                    matroid_matrix[i][j] = 1
        rank = compute_matroid(matroid_matrix)
        return rank
    
    def communication_complexity(f):
        # Simplified version of communication complexity calculation
        n = len(f)
        return n * (n - 1) // 2
    
    metric_name = "alexander_defect_vs_communication_complexity"
    instances_tested = 0
    total_alexander_defect = 0
    total_communication_complexity = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            f = generate_boolean_function(n)
            M = [[i] for i in range(n)]
            alexander_defect = compute_alexander_defect(M)
            communication_complexity_val = communication_complexity(f)
            
            total_alexander_defect += alexander_defect
            total_communication_complexity += communication_complexity_val
            instances_tested += 1
    
    mean_alexander_defect = Fraction(total_alexander_defect, instances_tested)
    mean_communication_complexity = Fraction(total_communication_complexity, instances_tested)
    
    correlation_coefficient = (instances_tested * mean_alexander_defect * mean_communication_complexity -
                               total_alexander_defect * total_communication_complexity) / \
                              math.sqrt((instances_tested * mean_alexander_defect**2 - total_alexander_defect**2) *
                                        (instances_tested * mean_communication_complexity**2 - total_communication_complexity**2))
    
    p_value = 1.0  # Placeholder for actual p-value calculation
    
    conjecture_holds = correlation_coefficient >= Fraction(7, 10) and p_value <= Fraction(5, 100)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
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
    
    def generate_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def num_true_assignments(formula, n):
        count = 0
        for i in range(2**n):
            assignment = format(i, f'0{n}b')
            if all(formula[j] == '0' or (assignment[int(j)] == '1') == (formula[j] == '1') for j in range(n)):
                count += 1
        return count
    
    def frege_proof_length(formula):
        # Simplified Frege proof length calculation (not actual Frege proof)
        return len(formula) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        num_resolutions = num_true_assignments(formula, n)
        proof_length = frege_proof_length(formula)
        results.append((num_resolutions, proof_length))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    num_resolutions = [r[0] for r in results]
    proof_lengths = [r[1] for r in results]
    
    mean_num_resolutions = sum(num_resolutions) / len(num_resolutions)
    mean_proof_lengths = sum(proof_lengths) / len(proof_lengths)
    
    covariance = sum((num_resolutions[i] - mean_num_resolutions) * (proof_lengths[i] - mean_proof_lengths) for i in range(len(results))) / len(results)
    variance_num_resolutions = sum((num_resolutions[i] - mean_num_resolutions) ** 2 for i in range(len(results))) / len(results)
    
    if variance_num_resolutions == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": len(num_resolutions),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_num_resolutions_zero"
        }
    
    correlation_coefficient = covariance / math.sqrt(variance_num_resolutions)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": abs(correlation_coefficient),
        "instances_tested": len(num_resolutions),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed + 1}")
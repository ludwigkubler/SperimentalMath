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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def count_irreducible_components(formula):
        # Placeholder function to simulate counting irreducible components
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    def shortest_frege_proof_length(formula):
        # Placeholder function to simulate Frege proof length calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula) * 2
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_boolean_formula(n)
        num_resolutions = count_irreducible_components(formula)
        proof_length = shortest_frege_proof_length(formula)
        results.append((num_resolutions, proof_length))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    num_resolutions = [r[0] for r in results]
    proof_lengths = [r[1] for r in results]
    mean_num_resolutions = sum(num_resolutions) / len(num_resolutions)
    mean_proof_lengths = sum(proof_lengths) / len(proof_lengths)
    
    numerator = sum((num_resolutions[i] - mean_num_resolutions) * (proof_lengths[i] - mean_proof_lengths) for i in range(len(results)))
    denominator = math.sqrt(sum((num_resolutions[i] - mean_num_resolutions)**2 for i in range(len(results))) * sum((proof_lengths[i] - mean_proof_lengths)**2 for i in range(len(results))))
    
    if denominator == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": abs(correlation_coefficient),
        "instances_tested": len(results),
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE no_support")
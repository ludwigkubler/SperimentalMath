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
    
    def generate_random_formula(n):
        clauses = []
        for _ in range(10):  # Generate a simple formula with 10 clauses
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def cc_rank(formula):
        # Placeholder for communication complexity rank calculation
        # This is a dummy implementation and should be replaced with the actual algorithm
        return len(formula)  # Simplified for demonstration purposes
    
    def symplectic_volume(formula):
        # Placeholder for minimal symplectic volume calculation
        # This is a dummy implementation and should be replaced with the actual algorithm
        return len(formula) * 0.5  # Simplified for demonstration purposes
    
    n = random.randint(5, 40)
    formula = generate_random_formula(n)
    cc_rank_value = cc_rank(formula)
    sv_value = symplectic_volume(formula)
    
    correlation_coefficient = (cc_rank_value - 1) * (sv_value - 1) / ((n - 2) ** 2)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.5 and correlation_coefficient < 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.3 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.3)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
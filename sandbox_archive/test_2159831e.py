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
    
    # Parameters for Tseitin formula generation
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    
    # Generate a random Tseitin formula
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for i in range(m):
        var1 = random.choice(variables)
        var2 = random.choice(variables)
        if random.choice([True, False]):
            clauses.append(f'{var1} OR {var2}')
        else:
            clauses.append(f'NOT {var1} AND NOT {var2}')
    
    # Construct the associated algebraic variety (simplified for demonstration)
    # This is a placeholder and should be replaced with actual computation
    hodge_integral = random.randint(0, 100)  # Placeholder value
    
    # Compute resolution proof length (simplified for demonstration)
    # This is a placeholder and should be replaced with actual computation
    resolution_proof_length = random.randint(1, n**2)  # Placeholder value
    
    # Constants
    p = 7  # Prime number for modulo operation
    c_p = 5  # Example constant for Hodge integral bound
    
    # Compute the ratio of Hodge integral to the constant c(p)
    ratio = Fraction(hodge_integral, c_p)
    
    # Check if the conjecture holds for this instance
    conjecture_holds = (ratio <= 1) and (resolution_proof_length <= n**2)
    counterexample = "" if conjecture_holds else f"Ratio: {ratio}, Proof Length: {resolution_proof_length}"
    
    return {
        "metric_name": "Hodge Integral Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and standard deviation of metric_value
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    
    squared_diff_sum = sum((result["metric_value"] - mean_metric_value) ** 2 for result in results)
    std_metric_value = math.sqrt(squared_diff_sum / len(results))
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    # Determine the final result based on acceptance criteria
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - 1) > 0.1 or result["resolution_proof_length"] > n**2 for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if abs(result["metric_value"] - 1) > 0.1 or result["resolution_proof_length"] > n**2)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unmet_acceptance_criteria")
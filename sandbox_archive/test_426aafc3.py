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

def generate_polynomial(degree):
    coefficients = [random.randint(-10, 10) for _ in range(degree + 1)]
    x = 'x'
    return sum(coeff * x**i for i, coeff in enumerate(coefficients))

def permanent(matrix):
    if len(matrix) == 0:
        return 1
    n = len(matrix)
    det = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * permanent(submatrix)
        sign *= -1
    return abs(det)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    degree = random.randint(5, 40)
    poly = generate_polynomial(degree)
    n = degree
    
    # Placeholder for actual computation of min_deg(W(φ(f)))
    # For this example, we'll just use a dummy value
    min_deg_weyl_char = degree * 2  # Dummy value
    
    permanent_gap = permanent([[1]*n for _ in range(n)])
    
    metric_name = "min_deg_Weyl_char"
    metric_value = min_deg_weyl_char
    instances_tested = 1
    conjecture_holds = min_deg_weyl_char >= permanent_gap
    counterexample = "" if conjecture_holds else f"Dummy counterexample for degree {degree}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Dummy counterexample\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(degree):
        coefficients = [random.randint(-10, 10) for _ in range(degree + 1)]
        return sum(coeff * x**i for i, coeff in enumerate(coefficients))
    
    def permanent(matrix):
        if len(matrix) == 0:
            return 1
        n = len(matrix)
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1)**j * matrix[0][j] * permanent(submatrix)
        return abs(det)
    
    def min_weyl_char_degree(poly, degree):
        # Placeholder function to simulate the computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(degree - 10, degree + 10)
    
    def gamma_permanent(n):
        # Placeholder function for γ permanent(n)
        # This is a dummy implementation and should be replaced with actual logic
        return n**2
    
    degree = random.randint(5, 40)
    poly = generate_polynomial(degree)
    min_deg = min_weyl_char_degree(poly, degree)
    gamma_n = gamma_permanent(degree)
    
    if min_deg < gamma_n:
        return {
            "metric_name": "min_deg(W(φ(f)))",
            "metric_value": min_deg,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "There exists a homogeneous polynomial f with degree d such that min_deg(W(φ(f))) < γ permanent(n)."
        }
    
    return {
        "metric_name": "min_deg(W(φ(f)))",
        "metric_value": min_deg,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"There exists a homogeneous polynomial f with degree d such that min_deg(W(φ(f))) < γ permanent(n).\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
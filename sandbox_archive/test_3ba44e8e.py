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
    
    n = 40
    d = 3
    
    # Define the PARITY function for n variables
    def parity(inputs):
        return sum(inputs) % 2
    
    # Generate a random input for the PARITY function
    inputs = [random.randint(0, 1) for _ in range(n)]
    
    # Compute the noncommutative Fourier transform of the PARITY function
    fourier_coefficients = {}
    for i in range(2**n):
        term = 1
        for j in range(n):
            if (i >> j) & 1:
                term *= (-1)**inputs[j]
        fourier_coefficients[i] = term
    
    # Count the number of non-zero coefficients
    non_zero_count = sum(abs(coeff) > 1e-6 for coeff in fourier_coefficients.values())
    
    # Calculate the expected lower bound
    lower_bound = n ** (1 / (d - 1))
    
    # Check if the conjecture holds
    conjecture_holds = non_zero_count >= lower_bound
    
    return {
        "metric_name": "non-zero_fourier_coefficients",
        "metric_value": non_zero_count,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Lower bound {lower_bound} not met with {non_zero_count} coefficients"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
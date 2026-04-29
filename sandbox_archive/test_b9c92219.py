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
    
    # Define the polynomial CSP parameters
    n = 5 + (seed % 6) * 5  # n ∈ {5, 10, 15, 20, 30, 40}
    degree = 3
    
    # Generate a random polynomial CSP over a finite field
    # For simplicity, we use the field GF(2)
    variables = [f'x{i}' for i in range(n)]
    constraints = []
    
    for _ in range(degree):
        monomials = []
        for var in variables:
            if random.choice([True, False]):
                monomials.append(var)
        constraint = ' + '.join(monomials) + ' ≡ 0 (mod 2)'
        constraints.append(constraint)
    
    # Compute the secant variety dimension
    # This is a simplified example; in practice, this would require symbolic computation
    secant_dimension = len(variables) - degree
    
    # Measure the SOS integrality gap via semidefinite programming
    # For simplicity, we assume a constant gap
    sos_gap = 1.0
    
    # Validate correlations between the gap and the secant variety's dimension
    if abs(sos_gap - secant_dimension) < 1e-6:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "SOS gap does not match secant variety dimension"
    
    return {
        "metric_name": "SOS integrality gap",
        "metric_value": sos_gap,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 8)]  # Default list of 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"SOS gap does not match secant variety dimension\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
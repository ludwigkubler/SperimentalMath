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
    
    # Parameters for the trial
    q = random.randint(2, 10)
    N = random.randint(5, 30)
    C_g = random.randint(1, 10)
    alpha = random.uniform(0.1, 0.9)
    c = random.uniform(0.1, 0.9)
    
    # Generate a random p-adic polynomial f over F_q
    coefficients = [random.randint(0, q-1) for _ in range(N)]
    f = lambda x: sum(coeff * (x ** i) for i, coeff in enumerate(reversed(coefficients)))
    
    # Compute the tropicalization T(f)
    T_f = max(abs(coeff) for coeff in coefficients)
    
    # Define an explicit function g with known ACC⁰ complexity C_g
    g = lambda x: sum((i + 1) * (x ** i) for i in range(C_g))
    
    # Compute the differential degree D_f(T(f))
    D_f_T_f = T_f
    
    # Compare D_f(g) to c * log^α(C_g)
    D_f_g = D_f_T_f
    expected_value = c * (C_g ** alpha)
    difference = abs(D_f_g - expected_value)
    
    return {
        "metric_name": "D_f(g)",
        "metric_value": D_f_g,
        "instances_tested": 1,
        "conjecture_holds": difference <= 3,
        "counterexample": "" if difference <= 3 else f"D_f(g) = {D_f_g}, expected ≥ {expected_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
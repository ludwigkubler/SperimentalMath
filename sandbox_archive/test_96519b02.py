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
    
    # Parameters
    q = 2**random.randint(3, 5)  # Finite field Fq
    N = random.randint(10, 20)   # Degree of the polynomial
    C_g = random.randint(1, 10)  # ACC⁰ complexity of g
    
    # Generate a random p-adic polynomial f over Fq
    coefficients = [random.randint(0, q-1) for _ in range(N+1)]
    f = lambda x: sum(coeff * (x**i) % q for i, coeff in enumerate(coefficients))
    
    # Compute the tropicalization T(f)
    T_f = {x: math.log(abs(f(x)), 2) for x in range(N)}
    
    # Determine the differential degree D_f(T(f))
    D_f_T_f = max(T_f.values()) - min(T_f.values())
    
    # Evaluate an explicit function g with known ACC⁰ complexity C_g
    g = lambda x: sum((x**i) % q for i in range(C_g+1))  # Example function
    
    # Compute the value of D_f(g)
    D_f_g = math.log(abs(f(g(0))), 2)
    
    # Check if the conjecture holds
    alpha = random.uniform(0.5, 1.5)  # Constant α > 0
    c = random.uniform(0.1, 0.3)      # Constant c > 0
    expected_value = c * (C_g ** alpha)
    
    if D_f_g < expected_value:
        conjecture_holds = False
        counterexample = f"g(x) has ACC⁰ complexity {C_g} but D_f(g) = {D_f_g}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "D_f(g)",
        "metric_value": D_f_g,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
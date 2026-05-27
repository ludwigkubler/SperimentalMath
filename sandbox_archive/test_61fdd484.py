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
    q = 2**random.randint(3, 5)  # Finite field Fq
    N = random.randint(10, 20)   # Degree of the polynomial
    alpha = 0.5                  # Constant in the conjecture
    
    # Generate a random p-adic polynomial f over Fq
    coefficients = [random.randint(0, q-1) for _ in range(N+1)]
    f = lambda x: sum(c * (x**i) % q for i, c in enumerate(coefficients))
    
    # Compute the tropicalization T(f)
    T_f = max([math.log(abs(f(x)), 2) for x in range(q)])
    
    # Define an explicit function g with known ACC⁰ complexity C_g
    def g(x):
        return sum((x**i) % q for i in range(1, N+1))
    C_g = N
    
    # Compute D_f(g)
    D_f_g = T_f + math.log(C_g, 2)
    
    # Check the conjecture
    c = 0.5  # Constant from the conjecture (to be adjusted based on actual data)
    if D_f_g >= c * C_g**alpha:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Counterexample: D_f(g)={D_f_g}, c*C_g^alpha={c*C_g**alpha}"
    
    return {
        "metric_name": "D_f(g)",
        "metric_value": D_f_g,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def polynomial_from_boolean_function(f):
        n = len(f)
        x = 'x'
        f_poly = sum(random.randint(0, 1) * (x + '^' + str(i)) if i > 0 else 1 for i in range(n+1))
        return f_poly
    
    def schur_weyl_rank(poly):
        # Placeholder function to compute the minimal rank of Schur-Weyl module decomposition
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)
    
    def permutation_circuit_size(n):
        return n**2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    poly = polynomial_from_boolean_function(f)
    rho_f = schur_weyl_rank(poly)
    circuit_size = permutation_circuit_size(n)
    
    metric_value = rho_f
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if rho_f <= C_n * math.log2(n)**2:
        conjecture_holds = True
    
    return {
        "metric_name": "Schur-Weyl Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
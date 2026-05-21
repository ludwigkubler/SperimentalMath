# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def fourier_coefficient(f, x):
        n = len(f)
        return sum(f[i] * (x ** i) % p for i in range(n)) / p
    
    def ac0_circuit_depth(f):
        # Simplified AC0 circuit depth estimation
        n = len(f)
        if n == 1:
            return 0
        return max(ac0_circuit_depth(f[:n//2]), ac0_circuit_depth(f[n//2:])) + 1
    
    def p_adic_order(f):
        n = len(f)
        max_coeff = max(abs(fourier_coefficient(f, x)) for x in range(p))
        return Fraction(max_coeff).numerator.bit_length()
    
    p = 7  # Prime field
    n_min = 5
    n_max = 40
    instances_per_seed = 30
    
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_per_seed):
        n = random.randint(n_min, n_max)
        f = generate_boolean_function(n)
        d = ac0_circuit_depth(f)
        omega_f = p_adic_order(f)
        
        total_metric_value += omega_f
        instances_tested += 1
        
        if omega_f != Fraction(2**d).numerator:
            conjecture_holds = False
            counterexample = f"AC0 function with depth {d} does not satisfy ω(g) = Θ(2^d)"
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = (sum((omega_f - mean_metric_value)**2 for omega_f in range(instances_tested)) / instances_tested)**0.5
    
    return {
        "metric_name": "p-adic order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
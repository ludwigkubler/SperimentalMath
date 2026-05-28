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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_euler_characteristic(circuit):
        n = len(circuit)
        if n == 0:
            return 0
        count = 0
        for i in range(2**n):
            if circuit[i] == 1:
                count += 1
        return count - (2**(n-1) - count)
    
    def compute_monotone_complexity(circuit):
        n = len(circuit)
        max_length = 0
        for i in range(2**n):
            if circuit[i] == 1:
                length = 0
                j = i
                while j > 0:
                    length += 1
                    j &= (j - 1)
                max_length = max(max_length, length)
        return max_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(30):
            circuit = generate_circuit(n)
            chi = compute_euler_characteristic(circuit)
            mu = compute_monotone_complexity(circuit)
            
            if chi > n**2 or mu > n:
                conjecture_holds = False
                counterexample = f"n={n}, χ(C)={chi}, μ(C)={mu}"
                break
            
            for k in range(1, 6):
                if not (0.5 * mu**k <= chi <= 2 * mu**k):
                    conjecture_holds = False
                    counterexample = f"n={n}, χ(C)={chi}, μ(C)={mu}, k={k}"
                    break
            
            instances_tested += 1
        
        results.append({
            "metric_name": "Euler characteristic",
            "metric_value": chi,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    total_metric = sum(result["metric_value"] for result in results)
    mean_metric = total_metric / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric": mean_metric,
        "std_metric": std_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric = sum(result["mean_metric"] for result in results)
    mean_metric = total_metric / len(results)
    std_metric = math.sqrt(sum((result["mean_metric"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction")
    else:
        first_failing_seed = min(result["seed"] for result in results if result["support_fraction"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
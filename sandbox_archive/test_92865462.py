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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def morse_function(f, x):
        n = len(f)
        return sum(abs(x[i] - f[x.index(i)]) for i in range(n))
    
    def geometric_entropy(morse_values, grid_size):
        n = len(morse_values)
        total = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if i != j:
                    total += abs(morse_values[i] - morse_values[j])
        return total / (n * (grid_size - 1))
    
    def frege_proof_size(f, max_length=10):
        n = len(f)
        proofs = []
        
        def dfs(path):
            if len(path) == n:
                if all(f[path[i]] == path[i] for i in range(n)):
                    proofs.append(path[:])
                return
            for j in range(2):
                path.append(j)
                dfs(path)
                path.pop()
        
        dfs([])
        return len(proofs)
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def property_P(f):
        # Placeholder for property P
        return any(f[i] != i for i in range(len(f)))
    
    results = []
    grid_size = 100
    
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        φ_f = [morse_function(f, x) for x in range(grid_size)]
        H_φ_f = geometric_entropy(φ_f, grid_size)
        s_f = frege_proof_size(f)
        
        results.append({
            "n": n,
            "H_φ_f": H_φ_f,
            "s_f": s_f
        })
    
    mean_H_φ_f = sum(result["H_φ_f"] for result in results) / len(results)
    std_H_φ_f = math.sqrt(sum((result["H_φ_f"] - mean_H_φ_f)**2 for result in results) / len(results))
    correlation = correlation_coefficient([result["H_φ_f"] for result in results], [result["s_f"] for result in results])
    
    conjecture_holds = correlation >= 0.7 and all(property_P(generate_boolean_function(n)) for _ in range(10) for n in range(5, 40))
    counterexample = "" if conjecture_holds else "property_P_undefined"
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_correlation = sum(result["metric_value"] for result in results) / len(results)
    std_correlation = math.sqrt(sum((result["metric_value"] - mean_correlation)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        counterexample = next(result for result in results if not result["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support_fraction")
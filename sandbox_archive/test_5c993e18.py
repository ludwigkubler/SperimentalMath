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
    
    def communication_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid Boolean function length")
        rank = 0
        for i in range(n):
            bits = [f[j] for j in range(2**n) if (j >> i) & 1]
            if sum(bits) > len(bits) / 2:
                rank += 1
        return rank
    
    def quaternionic_representation(f, size):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid Boolean function length")
        representation = []
        for i in range(size):
            if i < 2**n:
                representation.append((i, f[i]))
            else:
                representation.append((i, random.choice([0, 1])))
        return representation
    
    def approximation_error(representation, f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid Boolean function length")
        error = 0
        for i in range(2**n):
            approx = sum(x[1] for x in representation if (x[0] >> i) & 1)
            error += abs(approx - f[i])
        return error
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_rank(f)
        
        if r_f > n:
            k_max = 2 * n - 1
        else:
            k_max = int(r_f**2) + 1
        
        min_k = float('inf')
        best_representation = None
        
        for size in range(1, k_max + 1):
            representation = quaternionic_representation(f, size)
            error = approximation_error(representation, f)
            if error < min_k:
                min_k = error
                best_representation = representation
        
        results.append({
            "n": n,
            "r_f": r_f,
            "min_k": min_k,
            "best_representation": best_representation
        })
    
    mean_k = sum(result["min_k"] for result in results) / len(results)
    std_k = math.sqrt(sum((result["min_k"] - mean_k)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["min_k"] <= 4 * result["r_f"]**2 and result["best_representation"]) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "None found"
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_k,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_k = sum(result["metric_value"] for result in results) / len(results)
    std_k = math.sqrt(sum((result["metric_value"] - mean_k)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_k} std={std_k} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"None found\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data n_tested={len(results)}")
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
    
    def hamming_distance(a, b):
        return sum(x != y for x, y in zip(a, b))
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        min_cost = float('inf')
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    cost = hamming_distance(bin(i)[2:].zfill(n), bin(j)[2:].zfill(n))
                    min_cost = min(min_cost, cost)
        return min_cost
    
    def quaternionic_generators(f):
        n = int(math.log2(len(f)))
        generators = set()
        for i in range(2**n):
            if f[i] != f[(i ^ (1 << (n-1))) % 2**n]:
                generators.add(i)
        return len(generators)
    
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    primes = [i for i in range(5, 30) if is_prime(i)]
    
    results = []
    for n in primes:
        f = generate_boolean_function(n)
        comm_complexity = communication_complexity(f)
        gen_count = quaternionic_generators(f)
        
        results.append({
            "n": n,
            "communication_complexity": comm_complexity,
            "quaternionic_generators": gen_count
        })
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mean_comm = sum(r["communication_complexity"] for r in results) / len(results)
    mean_gen = sum(r["quaternionic_generators"] for r in results) / len(results)
    std_comm = math.sqrt(sum((r["communication_complexity"] - mean_comm)**2 for r in results) / len(results))
    std_gen = math.sqrt(sum((r["quaternionic_generators"] - mean_gen)**2 for r in results) / len(results))
    
    correlation = sum((r["communication_complexity"] - mean_comm) * (r["quaternionic_generators"] - mean_gen) for r in results) / len(results)
    correlation /= std_comm * std_gen
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation > 0.5 and correlation < -0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_comm = sum(r["metric_value"] for r in results) / len(results)
    std_comm = math.sqrt(sum((r["metric_value"] - mean_comm)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm} std={std_comm} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm} std={std_comm} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n']}, comm_complexity={r['communication_complexity']}, gen_count={r['quaternionic_generators']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
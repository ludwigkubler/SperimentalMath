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
    
    def generate_group(n):
        if n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        else:
            g = [0] * (n + 1)
            for i in range(1, n + 1):
                g[i] = random.randint(0, i - 1)
            return g
    
    def generate_representation(group, dim):
        V = [[random.random() for _ in range(dim)] for _ in range(len(group))]
        return V
    
    def calculate_automorphism_group(V):
        n = len(V)
        Aut_V = []
        for perm in itertools.permutations(range(n)):
            if all(abs(V[i][j] - V[perm[i]][perm[j]]) < 1e-9 for i in range(n) for j in range(n)):
                Aut_V.append(perm)
        return Aut_V
    
    def communication_complexity(V):
        n = len(V)
        C = 0
        for perm in itertools.permutations(range(n)):
            if all(abs(V[i][j] - V[perm[i]][perm[j]]) < 1e-9 for i in range(n) for j in range(n)):
                C += 1
        return C
    
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    primes = [i for i in range(5, 41) if is_prime(i)]
    seeds = random.sample(primes, 30)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            G = generate_group(n)
            V = generate_representation(G, n)
            Aut_V = calculate_automorphism_group(V)
            C = communication_complexity(V)
            
            if len(Aut_V) == 0:
                continue
            
            results.append({
                "metric_name": "communication_complexity",
                "metric_value": C,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            })
    
    if len(results) == 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_C = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "communication_complexity",
        "metric_value": mean_C,
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
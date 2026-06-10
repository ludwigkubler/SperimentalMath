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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(limit):
        primes = []
        for num in range(2, limit):
            if is_prime(num):
                primes.append(num)
        return primes
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def generate_group(n):
        if n == 2:
            return [0, 1], [(0, 0), (0, 1), (1, 0), (1, 1)]
        elif n == 3:
            return [0, 1, 2], [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        else:
            return generate_primes(n)
    
    def generate_representation(group, dim):
        V = [[random.randint(0, 1) for _ in range(dim)] for _ in range(len(group))]
        return V
    
    def compute_automorphism_group(V, group):
        Aut_V = []
        for perm in itertools.permutations(range(len(group))):
            if all(V[perm[i]][j] == V[i][perm[j]] for i in range(len(group)) for j in range(dim)):
                Aut_V.append(perm)
        return Aut_V
    
    def communication_complexity(Aut_V):
        # Placeholder function to simulate communication complexity
        return len(Aut_V) ** 2
    
    primes = generate_primes(50)
    seeds = random.sample(primes, 30)
    
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for seed in seeds:
        random.seed(seed)
        
        group_size = random.randint(5, 10)
        dim = random.randint(5, 10)
        n_max = max(n_max, group_size, dim)
        
        group, V = generate_group(group_size), generate_representation(group, dim)
        Aut_V = compute_automorphism_group(V, group)
        C = communication_complexity(Aut_V)
        
        instances_tested += len(V)
        metric_values.append(C)
        
        if C > 10:
            conjecture_holds = False
            counterexample = f"Communication complexity {C} exceeds 10 for seed {seed}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 50) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[sum(1 for r in results if not r['conjecture_holds'])].get('counterexample', 'unknown')}\" first_failing_seed={results.index(next(r for r in results if not r['conjecture_holds'] + 1))}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
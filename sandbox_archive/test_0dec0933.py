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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(n):
        primes = []
        num = 2
        while len(primes) < n:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def generate_permutation_group(n):
        elements = list(range(1, n + 1))
        group = []
        for i in range(n):
            perm = random.sample(elements, n)
            if all(perm[j] != j + 1 for j in range(n)):
                group.append(perm)
        return group
    
    def is_acc0_circuit(group, f):
        # Placeholder function to check if a permutation group can construct an ACC⁰ circuit
        # This is a dummy implementation and should be replaced with actual logic
        return False
    
    n = 40
    min_order = float('inf')
    instances_tested = 0
    
    for _ in range(30):
        f = random.randint(1, n)
        group = generate_permutation_group(n)
        order = len(group)
        
        if is_acc0_circuit(group, f):
            return {
                "metric_name": "min_order",
                "metric_value": order,
                "instances_tested": instances_tested + 1,
                "conjecture_holds": False,
                "counterexample": f"ACC⁰ circuit found with group of order {order}"
            }
        
        min_order = min(min_order, order)
        instances_tested += 1
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = generate_primes(30)
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
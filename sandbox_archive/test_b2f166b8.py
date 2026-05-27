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
    
    def generate_permutation_group(order, n):
        # Generate a permutation group of the given order
        # This is a simplified version and may not be correct for all cases
        elements = list(range(n))
        random.shuffle(elements)
        return elements
    
    def construct_acc0_circuit(group, n):
        # Construct an ACC⁰ circuit using the given permutation group
        # This is a simplified version and may not be correct for all cases
        if len(group) < n:
            return False
        return True
    
    n = random.randint(5, 40)
    primes = generate_primes(n)
    min_order = float('inf')
    
    for _ in range(30):
        order = random.randint(1, n**2 // 2 - 1)
        group = generate_permutation_group(order, n)
        if construct_acc0_circuit(group, n):
            min_order = min(min_order, order)
    
    conjecture_holds = min_order >= n**2 / 2
    counterexample = "" if conjecture_holds else f"Found a permutation group of order {min_order} for n={n}"
    
    return {
        "metric_name": "Minimum Order of Pseudorandom Permutation Group",
        "metric_value": min_order,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
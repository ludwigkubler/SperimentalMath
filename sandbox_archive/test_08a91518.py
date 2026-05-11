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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def projective_plane(q):
    points = [i for i in range(q**2 + q + 1)]
    lines = []
    for x in range(q**2 + q + 1):
        line = set()
        for y in range(q**2 + q + 1):
            if (x * y) % (q**2 + q + 1) == 0:
                line.add(x)
                line.add(y)
        lines.append(line)
    return points, lines

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q_values = [2, 3, 4]
    results = []
    
    for q in q_values:
        points, lines = projective_plane(q)
        num_lines = len(lines)
        
        # Simulate communication complexity using a basic protocol
        communication_complexity = 0
        
        for _ in range(10):  # Sample 10 random subsets of lines for each q
            subset1 = set(random.sample(lines, random.randint(1, num_lines // 2)))
            subset2 = set(random.sample(lines, random.randint(1, num_lines // 2)))
            
            # Check if the sets are disjoint
            is_disjoint = len(subset1.intersection(subset2)) == 0
            
            # Simulate communication (each player sends their subset size)
            communication_complexity += 2 * math.ceil(math.log(num_lines, 2))
        
        results.append({
            "q": q,
            "num_lines": num_lines,
            "communication_complexity": communication_complexity
        })
    
    mean_communication = sum(result["communication_complexity"] for result in results) / len(results)
    std_communication = math.sqrt(sum((result["communication_complexity"] - mean_communication) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(abs(result["communication_complexity"] - (q**2 * math.log(q))) < 10 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": mean_communication,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_communication = sum(result["metric_value"] for result in results) / len(results)
    std_communication = math.sqrt(sum((result["metric_value"] - mean_communication) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_communication} std={std_communication} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE no seeds supported the conjecture")
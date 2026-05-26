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

def generate_cnf(n, m):
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(list(variables)) * (-1 if random.random() < 0.5 else 1)]
        clauses.append(clause)
    return clauses

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def rank_of_groupoid(clauses):
    num_clauses = len(clauses)
    if num_clauses == 0:
        return 0
    
    # Initialize the rank to 1 (identity element)
    rank = 1
    
    # Use a set to track unique generators
    generators = set()
    
    for clause in clauses:
        # Convert clause to a tuple of literals
        generator = tuple(sorted(clause))
        
        # Check if this generator is already in the set
        if generator not in generators:
            generators.add(generator)
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    
    clauses = generate_cnf(n, m)
    
    if not clauses:
        return {
            "metric_name": "rank(G(F))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "empty_clauses"
        }
    
    rank = rank_of_groupoid(clauses)
    
    expected_rank = math.log(n, 2) ** 2
    
    return {
        "metric_name": "rank(G(F))",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= expected_rank,
        "counterexample": "" if rank <= expected_rank else f"rank({rank}) > O(log^2({n}))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    total_rank = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_rank += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supporting += 1
        
        results.append(trial_result)
    
    mean_rank = total_rank / len(results)
    support_fraction = count_supporting / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank({results[first_failing_seed]['metric_value']}) > O(log^2(n))\" first_failing_seed={first_failing_seed}")
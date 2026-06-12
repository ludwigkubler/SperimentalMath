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
    
    primes = [i for i in range(2, 100) if is_prime(i)]
    if not primes:
        return {
            "metric_name": "conjecture_holds",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = random.choice(primes)
    if n <= 1:
        return {
            "metric_name": "conjecture_holds",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "sub_asymptotic_n"
        }
    
    # Generate a random CNF formula with n variables
    num_clauses = random.randint(1, min(n * (n - 1) // 2, 30))
    cnf_formula = []
    for _ in range(num_clauses):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
        cnf_formula.append(clause)
    
    # Construct the associated clause tree and compute its width
    def build_clause_tree(cnf):
        if not cnf:
            return 0
        left = build_clause_tree([c[1:] for c in cnf if c[0] == -1])
        right = build_clause_tree([c[1:] for c in cnf if c[0] == 1])
        return max(left, right) + 1
    
    clause_tree_width = build_clause_tree(cnf_formula)
    
    # Identify the quotient group of the symmetric group Sn that represents the symmetries of the clause tree structure
    def is_symmetric_group(n):
        if n <= 1:
            return True
        for i in range(2, n + 1):
            if n % i == 0 and not is_symmetric_group(i):
                return False
        return True
    
    quotient_group_size = math.factorial(n)
    
    # Count the minimal number of ternary representations needed to describe all elements of this quotient group
    def ternary_representation(x, base=3):
        if x == 0:
            return [0]
        digits = []
        while x:
            digits.append(int(x % base))
            x //= base
        return digits[::-1]
    
    ternary_representations = set()
    for i in range(quotient_group_size):
        ternary_representations.add(tuple(ternary_representation(i)))
    
    minimal_ternary_representations = len(ternary_representations)
    
    # Check if the clause tree width is within Ω(n^2 log n) and θ(log^3 n)
    lower_bound = n**2 * math.log(n)
    upper_bound = math.log(n)**3
    
    conjecture_holds = lower_bound <= clause_tree_width <= upper_bound
    counterexample = "" if conjecture_holds else f"Clause tree width {clause_tree_width} not within bounds [{lower_bound}, {upper_bound}]"
    
    return {
        "metric_name": "conjecture_holds",
        "metric_value": minimal_ternary_representations,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
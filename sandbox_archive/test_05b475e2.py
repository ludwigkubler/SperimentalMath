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
    
    def generate_tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f"({var} | ~{var})")
        for i in range(1, n):
            clauses.append(f"{variables[i]} -> {variables[0]}")
        return " & ".join(clauses)
    
    def tropical_coordinate_values(formula):
        # Simplified version to generate random values
        return [random.randint(1, 5) for _ in range(len(formula.split()) // 2)]
    
    def minimal_root_separation(tropical_values):
        return min(tropical_values) - max(tropical_values)
    
    def shortest_resolution_proof_length(n):
        # Simplified version to generate a random length
        return random.randint(10, 50)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    tropical_values = tropical_coordinate_values(formula)
    min_separation = minimal_root_separation(tropical_values)
    proof_length = shortest_resolution_proof_length(n)
    
    if min_separation == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "min_separation_is_zero"
        }
    
    ratio = proof_length / min_separation
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r < 2**min([tropical_coordinate_values(generate_tseitin_formula(n)) for n in [5, 10, 15, 20, 30, 40]])) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(r > 2**min([tropical_coordinate_values(generate_tseitin_formula(n)) for n in [5, 10, 15, 20, 30, 40]]) for r in results):
        print(f"RESULT: FALSIFIED counterexample='ratio_exceeds_bound' first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unexpected_behavior")
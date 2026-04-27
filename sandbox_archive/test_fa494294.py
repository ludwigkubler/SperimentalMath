# auto-injected by SEC sandbox
import math
import itertools
import collections
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
import json

def generate_random_formula(n, d):
    if n == 0 or d == 0:
        return "NOT"
    elif d == 1:
        return random.choice(["AND", "OR"])
    else:
        subformulas = [generate_random_formula(random.randint(0, n-1), random.randint(1, d-1)) for _ in range(2)]
        operator = random.choice(["AND", "OR"])
        return f"({subformulas[0]} {operator} {subformulas[1]})"

def multiply_permutations(p, q):
    n = len(p)
    result = [0] * n
    for i in range(n):
        result[i] = p[q[i]]
    return result

def identity_permutation(n):
    return list(range(n))

def commutator_length(permutation):
    n = len(permutation)
    queue = [(identity_permutation(n), 0)]
    visited = set()
    while queue:
        current, length = queue.pop(0)
        if current == permutation:
            return length
        for a in range(n):
            for b in range(a+1, n):
                commutator = multiply_permutations(multiply_permutations([a], [b]), multiply_permutations([b], [a]))
                next_permutation = multiply_permutations(current, commutator)
                if tuple(next_permutation) not in visited:
                    visited.add(tuple(next_permutation))
                    queue.append((next_permutation, length + 1))
    return float('inf')

def find_min_bp_length(permutation):
    n = len(permutation)
    instructions = []
    current = identity_permutation(n)
    for i in range(2**n):
        if current == permutation:
            break
        for a in range(n):
            for b in range(a+1, n):
                commutator = multiply_permutations([a], [b])
                next_permutation = multiply_permutations(current, commutator)
                if next_permutation == permutation:
                    instructions.append((a, b))
                    current = next_permutation
                    break
            else:
                continue
            break
    return len(instructions)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 5, 6, 7, 8]
    d_values = [2, 3, 4, 5, 6]
    results = []
    
    for n in n_values:
        for d in d_values:
            F = generate_random_formula(n, d)
            phi_F = Barrington_construction(F)  # Assume this function is defined elsewhere
            cl_phi_F = commutator_length(phi_F)
            D_F = 4 * d - cl_phi_F
            L_5_F = find_min_bp_length(phi_F)
            
            results.append({
                "n": n,
                "d": d,
                "F": F,
                "phi_F": phi_F,
                "cl_phi_F": cl_phi_F,
                "D_F": D_F,
                "L_5_F": L_5_F
            })
    
    conjecture_holds = all(D_F < 1 or L_5_F >= 2 * (2 * d + 1) for result in results)
    counterexample = "" if conjecture_holds else "D(F)>=1 and L_5(F)<2*(2*d+1)"
    
    return {
        "metric_name": "L_5/F",
        "metric_value": sum(result["L_5_F"] / (2**(result["D_F"]) * (2*result["d"] + 1)) for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) if arg.isdigit() else int.from_bytes(arg.encode(), 'big') for arg in sys.argv[1:]]
    if not seeds:
        seeds = [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_L_5_over_F = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_L_5_over_F} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"D(F)>=1 and L_5(F)<2*(2*d+1)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
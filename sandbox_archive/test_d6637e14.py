# auto-injected by SEC sandbox
import itertools
import collections
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
import json
from sys import argv

def generate_random_dnf(n, k, implicant_size):
    variables = list(range(n))
    implicants = []
    
    while len(implicants) < k:
        implicant = set()
        for _ in range(implicant_size):
            var = random.choice(variables)
            if random.choice([True, False]):
                implicant.add(var)
            else:
                implicant.add(-var)
        
        if all(len(set(a).intersection(b)) == 0 for b in implicants):
            implicants.append(frozenset(implicant))
    
    return implicants

def recursive_minimum(truth_table, variables, memo):
    if len(variables) == 1:
        var = variables[0]
        return min(truth_table[var][True], truth_table[var][False])
    
    var = variables[0]
    memo_key = (var, tuple(sorted(variables[1:])))
    if memo_key in memo:
        return memo[memo_key]
    
    true_case = recursive_minimum(truth_table, variables[1:], memo)
    false_case = recursive_minimum(truth_table, variables[1:], memo)
    result = min(true_case, false_case)
    memo[memo_key] = result
    return result

def compute_möbius_number(lattice):
    n = len(lattice)
    mu = [0] * (2 ** n)
    mu[0] = 1
    
    for i in range(1, 2 ** n):
        for j in range(i):
            if lattice[j].issubset(i):
                mu[i] -= mu[j]
    
    return abs(mu[-1])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [6, 8, 10, 12]:
        for k in range(3, 9):
            for implicant_size in [2, 3, 4]:
                dnf = generate_random_dnf(n, k, implicant_size)
                
                truth_table = {var: {True: 0, False: 0} for var in range(n)}
                for implicant in dnf:
                    for assignment in range(1 << n):
                        if all((assignment >> i) & 1 == (abs(var) - 1) % 2 for var in implicant):
                            truth_table[implicant] += 1
                
                memo = {}
                depth = recursive_minimum(truth_table, list(range(n)), memo)
                
                lattice = [frozenset()]
                while True:
                    new_elements = set()
                    for element in lattice:
                        for i in range(n):
                            if (element | {i}) not in lattice:
                                new_elements.add(element | {i})
                    if not new_elements:
                        break
                    lattice.update(new_elements)
                
                mu_f = compute_möbius_number(lattice)
                required_depth = math.ceil(math.log2(1 + mu_f))
                
                results.append({
                    "n": n,
                    "k": k,
                    "implicant_size": implicant_size,
                    "depth": depth,
                    "mu_f": mu_f,
                    "required_depth": required_depth
                })
    
    total_depth = sum(result["depth"] for result in results)
    mean_depth = total_depth / len(results)
    std_dev = math.sqrt(sum((result["depth"] - mean_depth) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["depth"] >= result["required_depth"]) / len(results)
    
    conjecture_holds = support_fraction >= 0.99 and all(result["depth"] - result["required_depth"] >= 1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Depth",
        "metric_value": mean_depth,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, argv[1:])) if argv[1:] else [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"SEED": seed, **result}))
    
    total_depth = sum(result["depth"] for result in results)
    mean_depth = total_depth / len(results)
    std_dev = math.sqrt(sum((result["depth"] - mean_depth) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["depth"] >= result["required_depth"]) / len(results)
    
    if support_fraction >= 0.99 and all(result["depth"] - result["required_depth"] >= 1 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(result["depth"] > result["required_depth"] for result in results):
        first_failing_seed = seeds[next(i for i, result in enumerate(results) if result["depth"] > result["required_depth"])]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
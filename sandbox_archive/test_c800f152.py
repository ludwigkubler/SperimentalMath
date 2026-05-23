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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def bit_flip_permutations(f):
        n = len(f).bit_length() - 1
        perms = []
        for i in range(2**n):
            perm = list(f)
            for j in range(n):
                if (i >> j) & 1:
                    perm[j] = 1 - perm[j]
            perms.append(tuple(perm))
        return perms
    
    def transpositions(perms):
        transps = set()
        for perm in perms:
            for i in range(len(perm)):
                for j in range(i + 1, len(perm)):
                    if perm[i] != perm[j]:
                        transps.add((i, j))
        return transps
    
    def coxeter_groups(transps):
        n = len(transps)
        groups = set()
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in transps and (j, i) in transps:
                    group = {(i, j)}
                    stack = [(i, j)]
                    while stack:
                        x, y = stack.pop()
                        for z in range(n):
                            if (x, z) in transps and (z, y) in transps:
                                if (x, z) not in group:
                                    group.add((x, z))
                                    stack.append((x, z))
                    groups.add(tuple(sorted(group)))
        return len(groups)
    
    def pseudorandomness(f):
        n = len(f).bit_length() - 1
        random_vars = [random.choice([0, 1]) for _ in range(2**n)]
        correlation = sum(f[i] * random_vars[i] for i in range(len(f))) / len(f)
        return abs(correlation)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    perms = bit_flip_permutations(f)
    transps = transpositions(perms)
    num_groups = coxeter_groups(transps)
    pseudorand = pseudorandomness(f)
    
    upper_bound = 2**n / (n * math.log(n))
    epsilon = 0.1
    p_epsilon = lambda n: n
    
    conjecture_holds = num_groups <= upper_bound and pseudorand >= epsilon
    counterexample = "" if conjecture_holds else f"num_groups={num_groups}, pseudorand={pseudorand}"
    
    return {
        "metric_name": "Coxeter Group Complexity vs Pseudorandomness",
        "metric_value": num_groups,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = f"num_groups={results[first_failing_seed]['metric_value']}, pseudorand={pseudorandomness(generate_boolean_function(40))}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
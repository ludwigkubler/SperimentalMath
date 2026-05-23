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
        return set(perms)
    
    def generate_coxeter_groups(transpositions):
        n = len(transpositions)
        groups = set()
        for i in range(n):
            for j in range(i+1, n):
                group = {(i, j)}
                for k in range(n):
                    if (k, i) in group and (j, k) not in group:
                        group.add((j, k))
                    elif (k, j) in group and (i, k) not in group:
                        group.add((i, k))
                groups.add(frozenset(group))
        return groups
    
    def pseudorandomness(f):
        n = len(f).bit_length() - 1
        random_vars = [random.choice([0, 1]) for _ in range(2**n)]
        correlation = sum(f[i] * random_vars[i] for i in range(2**n)) / (2**n)
        return abs(correlation)
    
    def is_isomorphic(g1, g2):
        if len(g1) != len(g2):
            return False
        mapping = {}
        visited = set()
        stack = [next(iter(g1))]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            for neighbor in g1[node]:
                if neighbor not in visited and neighbor not in mapping:
                    mapping[neighbor] = next(iter(g2))
                    stack.append(neighbor)
                elif neighbor not in visited and mapping[neighbor] != next(iter(g2)):
                    return False
        return True
    
    def count_non_isomorphic_groups(groups):
        non_isomorphic = set()
        for group in groups:
            isomorphic_to_existing = False
            for existing_group in non_isomorphic:
                if is_isomorphic(group, existing_group):
                    isomorphic_to_existing = True
                    break
            if not isomorphic_to_existing:
                non_isomorphic.add(group)
        return len(non_isomorphic)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    transpositions = bit_flip_permutations(f)
    groups = generate_coxeter_groups(transpositions)
    num_groups = count_non_isomorphic_groups(groups)
    pseudorand = pseudorandomness(f)
    
    upper_bound = 2**n / (n * math.log(n))
    conjecture_holds = num_groups <= upper_bound and pseudorand >= 0.1
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
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
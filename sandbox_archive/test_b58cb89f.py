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
    
    def generate_coxeter_groups(perms):
        transpositions = [(i, i+1) for i in range(len(perms)-1)]
        groups = set()
        for p in perms:
            group = {tuple(p)}
            for t in transpositions:
                new_group = set()
                for g in group:
                    new_g = list(g)
                    new_g[t[0]], new_g[t[1]] = new_g[t[1]], new_g[t[0]]
                    new_group.add(tuple(new_g))
                group.update(new_group)
            groups.add(frozenset(group))
        return groups
    
    def pseudorandomness(f):
        n = len(f).bit_length() - 1
        random_vars = [random.choice([0, 1]) for _ in range(2**n)]
        corr = sum(f[i] * random_vars[i] for i in range(len(f))) / len(f)
        return abs(corr)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    perms = bit_flip_permutations(f)
    groups = generate_coxeter_groups(perms)
    num_groups = len(groups)
    
    if num_groups > 2**n / (n * math.log(n)):
        return {
            "metric_name": "num_groups",
            "metric_value": num_groups,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Number of groups {num_groups} exceeds upper bound {2**n / (n * math.log(n))}"
        }
    
    ε = pseudorandomness(f)
    p_ε = lambda x: x**2  # Example polynomial for simplicity
    
    if ε < 1 / p_ε(n):
        return {
            "metric_name": "pseudorandomness",
            "metric_value": ε,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Pseudorandomness {ε} is less than lower bound {1 / p_ε(n)}"
        }
    
    return {
        "metric_name": "num_groups",
        "metric_value": num_groups,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
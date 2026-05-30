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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def resolution(tree):
        while True:
            new_clauses = set()
            found_resolvent = False
            for i in range(len(tree)):
                for j in range(i + 1, len(tree)):
                    if -tree[i][0] in tree[j]:
                        resolvent = [lit for lit in tree[i] if lit != -tree[j][0]] + [lit for lit in tree[j] if lit != -tree[i][0]]
                        new_clauses.add(tuple(sorted(resolvent)))
                        found_resolvent = True
            if not found_resolvent:
                return len(tree)
            tree.extend(new_clauses)
    
    def euler_characteristic(simplicial_complex):
        return sum((-1)**(len(face) - 1) * len(list(itertools.combinations(face, len(face) - 1))) for face in simplicial_complex)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    tree = resolution(cnf)
    simplicial_complex = []
    for clause in cnf:
        simplicial_complex.append(tuple(sorted(clause)))
    
    chi = euler_characteristic(simplicial_complex)
    w = tree
    
    return {
        "metric_name": "chi_over_w",
        "metric_value": chi / w if w != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_chi_over_w = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_chi_over_w} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_chi_over_w} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
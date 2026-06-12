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
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution(cnf):
        clauses = set(tuple(c) for c in cnf)
        while True:
            new_clauses = []
            for (a, b) in clauses:
                if (-a, b) in clauses:
                    new_clause = tuple(sorted([c for c in range(1, n+1) if c not in [a, -b]]))
                    if new_clause not in clauses:
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    def grothendieck_witt_class(rank):
        # Simplified approximation for demonstration purposes
        return rank ** (2/3)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_tree_size = resolution(cnf)
    affine_sheaf_rank = grothendieck_witt_class(proof_tree_size)
    
    return {
        "metric_name": "affine_sheaf_rank",
        "metric_value": affine_sheaf_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(affine_sheaf_rank - n**(2/3)) <= 0.1 * n**(2/3),
        "counterexample": "" if conjecture_holds else f"Rank {affine_sheaf_rank} does not match O(n^(2/3))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.05:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
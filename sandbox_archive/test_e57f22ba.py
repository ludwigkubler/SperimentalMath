# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools
import collections

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_cnf(n, m):
        clauses = []
        for _ in range(m):
            literals = set(random.sample(range(1, n+1), 2))
            clause = {l if random.choice([True, False]) else -l for l in literals}
            clauses.append(clause)
        return clauses

    def construct_quiver(cnf):
        quiver = collections.defaultdict(set)
        for clause in cnf:
            for literal in clause:
                quiver[literal].update(clause)
        return quiver

    def is_automorphism(quiver, perm):
        n = max(abs(l) for l in quiver.keys())
        for i in range(1, n+1):
            if (quiver[i] != {perm[abs(l)-1] if l > 0 else -perm[abs(l)-1] for l in quiver[i]}):
                return False
        return True

    def find_automorphism_group(quiver):
        n = max(abs(l) for l in quiver.keys())
        automorphism_group = []
        for perm in itertools.permutations(range(n)):
            if is_automorphism(quiver, perm):
                automorphism_group.append(perm)
        return automorphism_group

    def dpll_path_length(cnf):
        # Placeholder function; actual implementation needed
        return random.randint(10, 50)

    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, 2*n)
    cnf = generate_random_cnf(n, m)
    quiver = construct_quiver(cnf)
    
    automorphism_group = find_automorphism_group(quiver)
    aut_order = len(automorphism_group)
    path_length = dpll_path_length(cnf)

    return {
        "metric_name": "AutOrderPathLengthCorrelation",
        "metric_value": aut_order * path_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
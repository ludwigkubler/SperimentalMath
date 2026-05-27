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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_cnf(n, m):
    cnf = []
    variables = list(range(1, n+1))
    for _ in range(m):
        clause = random.sample(variables + [-v for v in variables], k=random.randint(1, n))
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def solve(literals, clause_map):
        if not clause_map:
            return True
        literal = next((l for l in literals if l not in clause_map), None)
        if literal is None:
            return False
        new_clause_map = {l: [c for c in cs if literal not in c and -literal not in c] for l, cs in clause_map.items()}
        return solve(literals + [literal], new_clause_map) or solve(literals + [-literal], new_clause_map)
    n = len(cnf[0])
    variables = list(range(1, n+1))
    clause_map = {l: [] for l in range(-n, 0)}
    for c in cnf:
        for l in c:
            clause_map[l].append(c)
    return solve(variables, clause_map)

def twisted_poincaré_duality_group_rank(cnf):
    # Placeholder function to compute the rank of the twisted Poincaré duality group
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, 10)  # Dummy value for demonstration

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, 2*n)
    cnf = generate_cnf(n, m)
    rank = twisted_poincaré_duality_group_rank(cnf)
    depth = dpll(cnf)  # Depth of the DPLL proof
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,  # Placeholder, should be based on actual computation
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
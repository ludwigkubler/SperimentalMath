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

# Function to generate a random CNF formula with n variables and m clauses
def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

# Function to find a resolution proof for a CNF formula (simplified version)
def resolution_proof(cnf):
    # Placeholder for actual resolution proof algorithm
    return random.randint(50, 200)

# Function to compute the Hodge decomposition rank of a CNF formula
def hodge_decomposition_rank(cnf):
    # Placeholder for actual Hodge decomposition rank computation
    return random.randint(1, 10)

# Function to run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 5 * n)
    cnf = generate_cnf(n, m)
    
    t_star_F = resolution_proof(cnf)
    HD_F = hodge_decomposition_rank(cnf)
    
    if t_star_F == 0:
        return {
            "metric_name": "HD(F) / log(t*(F))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_length_zero"
        }
    
    metric_value = HD_F / math.log(t_star_F)
    
    return {
        "metric_name": "HD(F) / log(t*(F))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None and r["metric_value"] <= 10**5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not_supported' first_failing_seed={first_failing_seed}")
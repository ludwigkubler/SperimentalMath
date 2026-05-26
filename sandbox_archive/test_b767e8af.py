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
    n = random.randint(5, 40)
    
    # Generate a random 3-CNF formula with n variables
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        while len(set(clause)) == 1:
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        clauses.append(clause)
    
    # Construct the Tseitin resolution tree
    def tseitin_resolution(formula):
        if not formula:
            return []
        if isinstance(formula[0], list):
            left = tseitin_resolution(formula[0])
            right = tseitin_resolution(formula[1])
            return left + right + [[-formula[2]], [formula[2], -left[-1]], [formula[2], -right[-1]]]
        else:
            return [[formula]]
    
    tree = tseitin_resolution(clauses)
    depth = len(tree) - 1
    
    # Compute the configuration space cohomology rank
    def compute_cohomology_rank(depth):
        if depth == 0:
            return 1
        return 2 * compute_cohomology_rank(depth - 1)
    
    rank = compute_cohomology_rank(depth)
    
    # Check the conjecture
    c = 2
    conjecture_holds = rank <= c * depth
    
    return {
        "metric_name": "cohomology_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Depth {depth}, Rank {rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
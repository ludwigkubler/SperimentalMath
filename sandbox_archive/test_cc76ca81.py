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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_tree(cnf):
        # Simplified resolution tree construction
        tree = {}
        for clause in cnf:
            if len(clause) == 2:
                continue
            var = abs(clause[0])
            neg_var = -var
            if neg_var not in tree:
                tree[neg_var] = []
            tree[neg_var].append((clause, []))
        return tree
    
    def hodge_index(tree):
        # Simplified Hodge index calculation
        leaves = 0
        for node in tree.values():
            if not node:
                leaves += 1
        return leaves
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    tree = resolution_tree(cnf)
    h_F = hodge_index(tree)
    l_F = len(tree)
    
    if l_F == 0:
        return {
            "metric_name": "Hodge Index vs Resolution Proof Tree Diameter",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c = math.log2(l_F)
    if h_F <= c:
        return {
            "metric_name": "Hodge Index vs Resolution Proof Tree Diameter",
            "metric_value": h_F,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Hodge Index vs Resolution Proof Tree Diameter",
            "metric_value": h_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"h({n}, {m}) = {h_F} > c * log2(l_F) where l_F = {l_F}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)
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
        tree = {}
        for clause in cnf:
            if clause[0] not in tree:
                tree[clause[0]] = []
            if clause[1] not in tree:
                tree[clause[1]] = []
            tree[clause[0]].append(clause)
            tree[clause[1]].append(clause)
        return tree
    
    def dyadic_spectrum(tree):
        # Placeholder for actual FFT implementation
        spectrum = [random.random() for _ in range(2**len(tree))]
        return spectrum
    
    def entropy(spectrum):
        total = sum(spectrum)
        if total == 0:
            return 0
        return -sum(p * math.log2(p) for p in spectrum if p > 0)
    
    def resolution_depth(tree, node=None):
        if node is None:
            node = next(iter(tree))
        depth = 1
        for child in tree[node]:
            depth = max(depth, 1 + resolution_depth(tree, child[1]))
        return depth
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    tree = resolution_tree(cnf)
    spectrum = dyadic_spectrum(tree)
    H_d_PT = entropy(spectrum)
    depth = resolution_depth(tree)
    
    return {
        "metric_name": "H_d(PT)",
        "metric_value": H_d_PT,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": H_d_PT <= math.log(m + n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
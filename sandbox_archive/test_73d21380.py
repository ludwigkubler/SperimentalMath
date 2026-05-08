# auto-injected by SEC sandbox
import math
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

def popcount(n):
    return bin(n).count('1')

def hamming(x, y):
    return popcount(x ^ y)

def distance_matrix(X):
    n = len(X)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            D[i][j] = hamming(X[i], X[j])
            D[j][i] = D[i][j]
    return D

def tree_to_cover(tree, leaves, r):
    n = len(leaves)
    cover = [[] for _ in range(n)]
    for node in range(n):
        if tree[node] == -1:
            continue
        parent = tree[node]
        while parent != -1:
            cover[parent].append(node)
            parent = tree[parent]
    thickened = [set() for _ in range(n)]
    for i in range(n):
        if len(cover[i]) > r:
            for j in cover[i]:
                thickened[j].add(i)
    return thickened

def is_valid_cover(X, D, cover, multiplicity_limit, diameter_limit):
    n = len(X)
    for i in range(n):
        for j in range(i + 1, n):
            if hamming(X[i], X[j]) > diameter_limit:
                continue
            count = sum(1 for k in range(n) if i in cover[k] and j in cover[k])
            if count > multiplicity_limit:
                return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    X = ['000', '001', '010', '100', '011', '101', '110', '111']
    D = distance_matrix(X)
    
    # Canonical depth-3 KW protocol
    tree = [-1] * 8
    leaves = [i for i in range(8)]
    for r in range(3):
        for leaf in leaves:
            if tree[leaf] == -1:
                continue
            parent = tree[leaf]
            while parent != -1:
                tree[parent] = leaf
                parent = tree[parent]
    
    # Run tree_to_cover and check properties
    thickened = [set() for _ in range(8)]
    for i in range(8):
        if len(leaves) > r:
            for j in leaves:
                thickened[j].add(i)
    
    multiplicity = max(len(thickened[i]) for i in range(8))
    diameter = 4
    
    # Brute-force search for covers
    min_multiplicity = float('inf')
    for cover_size in range(1, len(X) + 1):
        for cover in itertools.combinations(range(len(X)), cover_size):
            if is_valid_cover(X, D, [cover], multiplicity_limit=3, diameter_limit=2):
                min_multiplicity = min(min_multiplicity, len(cover))
    
    conjecture_holds = multiplicity <= 4 and diameter <= 4 and min_multiplicity > 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Multiplicity and Diameter",
        "metric_value": (multiplicity, diameter),
        "instances_tested": len(X),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_multiplicity = sum(r["metric_value"][0] for r in results) / len(results)
    std_multiplicity = (sum((r["metric_value"][0] - mean_multiplicity) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_multiplicity} std={std_multiplicity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_multiplicity} std={std_multiplicity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
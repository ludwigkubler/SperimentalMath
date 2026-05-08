# auto-injected by SEC sandbox
import math
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from collections import defaultdict

def popcount(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def hamming(x, y):
    return popcount(int(x, 2) ^ int(y, 2))

def distance_matrix(X):
    n = len(X)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            D[i][j] = hamming(X[i], X[j])
            D[j][i] = D[i][j]
    return D

def tree_to_cover(tree, leaves, r):
    cover = defaultdict(list)
    queue = [(node, r) for node in leaves if tree[node]['depth'] == 0]
    while queue:
        node, r = queue.pop(0)
        cover[r].append(node)
        for child in tree[node]['children']:
            queue.append((child, r - 1))
    return cover

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    X = ['000', '001', '010', '100', '011', '101', '110', '111']
    D = distance_matrix(X)
    
    # Construct the depth-3 KW protocol tree
    leaves = list(range(len(X)))
    tree = {i: {'depth': 0, 'children': []} for i in range(len(X))}
    for i in range(4):
        new_leaves = []
        for leaf in leaves:
            x = X[leaf]
            if i == 0:
                child1 = len(tree)
                tree[child1] = {'depth': i + 1, 'children': []}
                tree[leaf]['children'].append(child1)
                new_leaves.append(child1)
                child2 = len(tree)
                tree[child2] = {'depth': i + 1, 'children': []}
                tree[leaf]['children'].append(child2)
                new_leaves.append(child2)
            else:
                child = len(tree)
                tree[child] = {'depth': i + 1, 'children': []}
                tree[leaf]['children'].append(child)
                new_leaves.append(child)
        leaves = new_leaves
    
    # Run tree_to_cover for r = 1, 2, 3
    covers = [tree_to_cover(tree, leaves, r) for r in range(1, 4)]
    
    # Check multiplicity and diameter
    multiplicity = max(len(covers[r][r]) for r in range(1, 4))
    diameter = max(max(D[leaf1][leaf2] for leaf2 in covers[r][r]) for r in range(1, 4))
    
    # Brute-force search for covers of size <= 8 with set diameter <= 2
    def brute_force():
        from itertools import combinations
        for cover_size in range(1, 9):
            for cover in combinations(range(len(X)), cover_size):
                if all(D[leaf1][leaf2] <= 2 for leaf1, leaf2 in combinations(cover, 2)):
                    multiplicity = max(multiplicity for leaf in cover)
        return multiplicity
    
    brute_multiplicity = brute_force()
    
    # Determine if the conjecture holds
    conjecture_holds = multiplicity <= 4 and diameter <= 4 and brute_multiplicity > 3
    
    return {
        "metric_name": "Multiplicity and Diameter",
        "metric_value": (multiplicity, diameter),
        "instances_tested": len(X),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Multiplicity {brute_multiplicity} > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_multiplicity = sum(r['metric_value'][0] for r in results) / len(results)
    std_multiplicity = (sum((r['metric_value'][0] - mean_multiplicity)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_multiplicity} std={std_multiplicity} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity {results[first_failing_seed]['metric_value'][0]} > 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
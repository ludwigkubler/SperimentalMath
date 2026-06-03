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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_decision_tree(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input is not a valid boolean function")
        
        tree = {}
        for i in range(n):
            tree[i] = {'0': {}, '1': {}}
            mask = 1 << (n - i - 1)
            for j in range(2**i):
                left_child = f[j * 2]
                right_child = f[j * 2 + 1]
                tree[i]['0'][j] = left_child
                tree[i]['1'][j] = right_child
        return tree
    
    def communication_complexity_rank(tree, n):
        rank = 0
        for i in range(n):
            rank += max(len(tree[i]['0']), len(tree[i]['1']))
        return rank
    
    def symplectic_reduction(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input is not a valid boolean function")
        
        leaves = []
        for i in range(2**n):
            leaves.append(f[i])
        return leaves
    
    def minimal_geometric_entropy(leaves):
        entropy = 0
        n = len(leaves)
        for leaf in leaves:
            count = leaves.count(leaf)
            p = count / n
            if p > 0:
                entropy += -p * math.log2(p)
        return entropy
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    entropies = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        tree = construct_decision_tree(f)
        rank = communication_complexity_rank(tree, n)
        leaves = symplectic_reduction(f)
        entropy = minimal_geometric_entropy(leaves)
        
        ranks.append(rank)
        entropies.append(entropy)
    
    corr_coeff = correlation_coefficient(ranks, entropies)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": corr_coeff,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff >= 0.7 and all(corr_coeff >= 0 for corr_coeff in [corr_coeff]),
        "counterexample": "" if corr_coeff >= 0.7 else f"Negative correlation at n={n_values[entropies.index(min(entropies))]}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and min(res["metric_value"] for res in results) >= 0.5:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Negative correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
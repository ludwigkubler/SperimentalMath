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
    
    def generate_and_or_tree(depth, branching_factor):
        if depth == 1:
            return random.choice(['0', '1'])
        else:
            root = random.choice(['AND', 'OR'])
            children = [generate_and_or_tree(depth - 1, branching_factor) for _ in range(branching_factor)]
            return (root, children)
    
    def tropicalize(tree):
        if isinstance(tree, str):
            return tree
        elif tree[0] == 'AND':
            return max(tropicalize(child) for child in tree[1:])
        else:
            return min(tropicalize(child) for child in tree[1:])
    
    def lie_algebra_rank(tropicalized_tree):
        if tropicalized_tree == '0' or tropicalized_tree == '1':
            return 0
        elif isinstance(tropicalized_tree, str):
            return 1
        else:
            ranks = [lie_algebra_rank(child) for child in tropicalized_tree[1:]]
            return max(ranks) + 1
    
    def spearman_correlation(x, y):
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        n = len(x)
        d_squared_sum = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        rho_numerator = 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
        return rho_numerator
    
    depths = [5, 10, 15, 20, 30, 40]
    branching_factors = [2, 5, 10, 15, 20]
    instances_tested = 0
    total_rank = 0
    ranks = []
    
    for depth in depths:
        for _ in range(5):
            tree = generate_and_or_tree(depth, random.choice(branching_factors))
            tropicalized = tropicalize(tree)
            rank = lie_algebra_rank(tropicalized)
            instances_tested += 1
            total_rank += rank
            ranks.append(rank)
    
    mean_value = total_rank / instances_tested
    rho = spearman_correlation(ranks, [depth for depth in depths for _ in range(5)])
    
    conjecture_holds = abs(rho) > 0.9
    counterexample = "" if conjecture_holds else "rho={:.2f}".format(rho)
    
    return {
        "metric_name": "spearman_correlation",
        "metric_value": rho,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='rho={:.2f}' first_failing_seed={}".format(r["metric_value"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={:.2f}".format(support_fraction))
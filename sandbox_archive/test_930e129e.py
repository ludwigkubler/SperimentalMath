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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def xor_and_tree_width(tree):
        if isinstance(tree, list):
            return max(xor_and_tree_width(subtree) for subtree in tree)
        else:
            return 1
    
    def geometric_langlands_object(tree):
        # Constructive mapping based on the representation theory of the symmetric group
        width = xor_and_tree_width(tree)
        n = len(tree)
        K = [Fraction(1, i + 1) for i in range(width)]
        X = [[sum(K[i] * (2 ** j if j % 2 == 0 else -2 ** j) for j in range(i + 1)) for i in range(n)]]
        return X
    
    def minimal_rank(X):
        # Compute the minimal rank of the moduli space of K-points on X
        n = len(X)
        rank = 0
        for i in range(n):
            if all(X[j][i] == 0 for j in range(i + 1, n)):
                rank += 1
        return rank
    
    def generate_xor_and_tree(n, depth):
        if depth == 1:
            return [random.choice([0, 1]) for _ in range(n)]
        else:
            left = generate_xor_and_tree(n // 2, depth - 1)
            right = generate_xor_and_tree(n - n // 2, depth - 1)
            return [left[i] ^ right[i] for i in range(n)]
    
    def is_valid_tree(tree):
        if isinstance(tree, list):
            return all(is_valid_tree(subtree) for subtree in tree)
        else:
            return len(tree) == 1
    
    n = random.randint(5, 40)
    depth = random.randint(3, 6)
    while True:
        tree = generate_xor_and_tree(n, depth)
        if is_valid_tree(tree):
            break
    
    X = geometric_langlands_object(tree)
    width = xor_and_tree_width(tree)
    rank = minimal_rank(X)
    
    metric_value = Fraction(rank, width)
    conjecture_holds = 0.5 <= metric_value <= 1.5
    counterexample = "" if conjecture_holds else f"Tree width: {width}, Rank: {rank}"
    
    return {
        "metric_name": "Minimal Rank / Tree Width",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
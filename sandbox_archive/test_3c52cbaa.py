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
    
    def generate_tseitin_tree(w, h):
        if w == 0 or h == 0:
            return []
        tree = [random.randint(1, 2)]
        for _ in range(h - 1):
            new_level = []
            for node in tree:
                if random.choice([True, False]):
                    new_level.append(node * 2)
                else:
                    new_level.append(node * 2 + 1)
            tree.extend(new_level)
        return tree
    
    def deligne_lusztig_cone(tree):
        n = len(tree)
        cone = [[0] * (n + 1) for _ in range(n + 1)]
        cone[0][0] = 1
        for i in range(1, n + 1):
            cone[i][i] = 1
            for j in range(i):
                cone[i][j] = cone[j][i]
        return cone
    
    def min_rank(cone):
        rank = 0
        while True:
            found = False
            for i in range(len(cone)):
                if any(x != 0 for x in cone[i]):
                    row_sum = sum(abs(x) for x in cone[i])
                    for j in range(i + 1, len(cone)):
                        if all(x == 0 for x in cone[j]):
                            continue
                        col_sum = sum(abs(x) for x in [cone[k][j] for k in range(len(cone)) if cone[k][i] != 0])
                        if row_sum <= col_sum:
                            found = True
                            break
                    if not found:
                        rank += 1
                        break
            if not found:
                break
        return rank
    
    def tseitin_resolution_tree_width(tree):
        width = 0
        for node in tree:
            if node % 2 == 0:
                width += 1
            else:
                width -= 1
        return abs(width)
    
    def tseitin_resolution_tree_height(tree):
        height = 0
        current_level = [tree[0]]
        while current_level:
            next_level = []
            for node in current_level:
                if node % 2 == 0:
                    next_level.extend([node * 2, node * 2 + 1])
                else:
                    next_level.extend([node * 2, node * 2 + 1])
            current_level = next_level
            height += 1
        return height
    
    def deligne_lusztig_cone_upper_bound(w, h):
        return w**2 / h
    
    n = random.randint(5, 40)
    tree = generate_tseitin_tree(n // 2, n // 2)
    width = tseitin_resolution_tree_width(tree)
    height = tseitin_resolution_tree_height(tree)
    
    cone = deligne_lusztig_cone(tree)
    rank = min_rank(cone)
    upper_bound = deligne_lusztig_cone_upper_bound(width, height)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= upper_bound,
        "counterexample": "" if rank <= upper_bound else f"Rank {rank} exceeds upper bound {upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
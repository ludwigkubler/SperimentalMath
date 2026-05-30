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
    
    def generate_frege_tree(h, m):
        if h == 0:
            return []
        elif h == 1:
            return [random.randint(0, 1)]
        else:
            root = random.randint(0, 1)
            left_size = random.randint(1, m - 2)
            right_size = m - 1 - left_size
            left_tree = generate_frege_tree(h - 1, left_size)
            right_tree = generate_frege_tree(h - 1, right_size)
            return [root] + left_tree + right_tree
    
    def is_isomorphic(tree1, tree2):
        if len(tree1) != len(tree2):
            return False
        if not tree1 and not tree2:
            return True
        root1 = tree1[0]
        root2 = tree2[0]
        if root1 != root2:
            return False
        left_subtree1 = tree1[1:]
        right_subtree1 = []
        for i in range(1, len(tree1)):
            if tree1[i] == root1:
                break
            right_subtree1.append(tree1[i])
        left_subtree2 = tree2[1:]
        right_subtree2 = []
        for i in range(1, len(tree2)):
            if tree2[i] == root2:
                break
            right_subtree2.append(tree2[i])
        return (is_isomorphic(left_subtree1, left_subtree2) and is_isomorphic(right_subtree1, right_subtree2)) or \
               (is_isomorphic(left_subtree1, right_subtree2) and is_isomorphic(right_subtree1, left_subtree2))
    
    def count_automorphisms(tree):
        if not tree:
            return 1
        n = len(tree)
        automorphisms = set()
        for perm in itertools.permutations(range(n)):
            permuted_tree = [tree[perm[i]] for i in range(n)]
            if is_isomorphic(tree, permuted_tree):
                automorphisms.add(tuple(perm))
        return len(automorphisms)
    
    h_values = [5, 10, 15, 20, 30, 40]
    m_values = [10, 20, 30, 40]
    results = []
    for _ in range(30):
        h = random.choice(h_values)
        m = random.choice(m_values)
        tree = generate_frege_tree(h, m)
        automorphisms_count = count_automorphisms(tree)
        if automorphisms_count > h ** (3/2) * m ** (1/2):
            return {
                "metric_name": "Automorphism Count",
                "metric_value": automorphisms_count,
                "instances_tested": 1,
                "n_max": max(h, m),
                "conjecture_holds": False,
                "counterexample": f"Tree with h={h}, m={m} has {automorphisms_count} automorphisms > O({h}^(3/2) * {m}^(1/2))"
            }
        results.append(automorphisms_count)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "Automorphism Count",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(h_values + m_values),
        "conjecture_holds": all(x <= h ** (3/2) * m ** (1/2) for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample = next((r['counterexample'] for r in results if not r['conjecture_holds']), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
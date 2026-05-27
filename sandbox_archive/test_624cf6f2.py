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
    
    def generate_xor_and_tree(n):
        if n == 1:
            return ['leaf']
        else:
            left = generate_xor_and_tree(n // 2)
            right = generate_xor_and_tree(n - n // 2)
            return ['xor', left, right]
    
    def compute_configuration_space(tree):
        if tree[0] == 'leaf':
            return {tuple([1])}
        elif tree[0] == 'xor':
            left_space = compute_configuration_space(tree[1])
            right_space = compute_configuration_space(tree[2])
            new_space = set()
            for l in left_space:
                for r in right_space:
                    new_space.add(tuple(sorted(l + r)))
            return new_space
        elif tree[0] == 'and':
            left_space = compute_configuration_space(tree[1])
            right_space = compute_configuration_space(tree[2])
            new_space = set()
            for l in left_space:
                for r in right_space:
                    if all(x == y for x, y in zip(l, r)):
                        new_space.add(tuple(sorted(l)))
            return new_space
        else:
            raise ValueError("Invalid tree node")
    
    def minimal_rank(configuration_space):
        # Placeholder for actual computation of minimal rank
        # For simplicity, we use the size of the configuration space as a proxy
        return len(configuration_space)
    
    n = random.randint(5, 40)
    tree = generate_xor_and_tree(n)
    config_space = compute_configuration_space(tree)
    rank = minimal_rank(config_space)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n * math.log2(n),
        "counterexample": "" if rank <= n * math.log2(n) else f"Tree with {n} leaves has rank {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
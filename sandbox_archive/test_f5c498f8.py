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
            return 'x'
        else:
            left = generate_xor_and_tree(n // 2)
            right = generate_xor_and_tree((n + 1) // 2)
            return f'({left} {random.choice(["&", "|"])} {right})'
    
    def tropicalize(tree):
        if tree[0] == '(' and tree[-1] == ')':
            left, op, right = tree[1:-1].split()
            if op == '&':
                return max(tropicalize(left), tropicalize(right))
            elif op == '|':
                return min(tropicalize(left), tropicalize(right))
        else:
            return int(tree)
    
    def minimal_rank(tree):
        rank = tropicalize(tree)
        return rank
    
    n = random.randint(1, 40)
    tree = generate_xor_and_tree(n)
    rank = minimal_rank(tree)
    
    result = {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= math.log2(n) and (rank == 1 if n == 40 else True),
        "counterexample": "" if rank <= math.log2(n) and (rank == 1 if n == 40 else True) else f"n={n}, rank={rank}"
    }
    
    return result

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(6)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
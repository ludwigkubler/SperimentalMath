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
            return f'({left} & {right}) | ({left} & ~{right})'
    
    def tropicalize(tree):
        if tree.startswith('(') and tree.endswith(')'):
            left, op, right = tree[1:-1].split()
            if op == '&':
                return max(tropicalize(left), tropicalize(right))
            elif op == '|':
                return min(tropicalize(left), tropicalize(right))
        else:
            return int(tree)
    
    def minimal_rank(tree):
        return tropicalize(tree)
    
    n = random.randint(1, 40)
    tree = generate_xor_and_tree(n)
    rank = minimal_rank(tree)
    
    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= math.log2(n) and (n <= 40 or rank == 1)
    counterexample = "" if conjecture_holds else f"rank={rank}, expected=Θ(log({n})) or O(1)"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result['metric_value'] for result in results) / len(results)
    std_dev = math.sqrt(sum((result['metric_value'] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
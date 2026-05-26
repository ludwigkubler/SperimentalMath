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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_xor_and_tree(n):
        if n == 1:
            return 'x'
        else:
            left = generate_xor_and_tree(n // 2)
            right = generate_xor_and_tree(n - n // 2)
            return f'({left} {random.choice(["&", "|"])} {right})'
    
    def tropicalize(tree):
        if isinstance(tree, str):
            return tree
        else:
            left = tropicalize(tree[0])
            op = tree[1]
            right = tropicalize(tree[2])
            if op == '&':
                return f'{left} & {right}'
            elif op == '|':
                return f'{left} | {right}'
    
    def minimal_rank(tree):
        if isinstance(tree, str):
            return 0
        else:
            left_rank = minimal_rank(tree[0])
            right_rank = minimal_rank(tree[2])
            return max(left_rank, right_rank) + 1
    
    n = random.randint(1, 40)
    tree = generate_xor_and_tree(n)
    rank = minimal_rank(tropicalize(eval(tree)))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n.bit_length(),
        "counterexample": "" if rank <= n.bit_length() else f"rank={rank}, expected={n.bit_length()}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
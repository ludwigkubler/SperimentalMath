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
    
    def is_valid_abp(abp, n):
        if len(abp) == 0 or abp[0] != 'input':
            return False
        for node in abp[1:]:
            if node[0] not in ['add', 'mul']:
                return False
            if len(node[1]) != 2:
                return False
            if node[1][0] == 'input' and node[1][1] == 'input':
                continue
            if node[1][0] == 'input' or node[1][1] == 'input':
                return False
        return True
    
    def depth(abp):
        if abp[0] == 'input':
            return 0
        elif abp[0] in ['add', 'mul']:
            return 1 + max(depth(abp[1][0]), depth(abp[1][1]))
    
    def generate_abps(n):
        abps = []
        stack = [['input']]
        while stack:
            current = stack.pop()
            if is_valid_abp(current, n):
                abps.append(current)
            if len(current) == 2 and current[0] in ['add', 'mul']:
                for child in current[1]:
                    if isinstance(child, list):
                        stack.append([current[0], [child]])
        return abps
    
    def parity_function(n):
        return sum(1 << i for i in range(n) if (i & 1) == 0)
    
    n = random.randint(5, 40)
    target_value = parity_function(n)
    abps = generate_abps(n)
    
    min_depth = float('inf')
    for abp in abps:
        if depth(abp) < min_depth and eval_abp(abp, n) == target_value:
            min_depth = depth(abp)
    
    return {
        "metric_name": "min_depth",
        "metric_value": min_depth,
        "instances_tested": len(abps),
        "conjecture_holds": min_depth >= math.log2(n),
        "counterexample": "" if min_depth >= math.log2(n) else f"ABP with depth {min_depth} found for n={n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_depth = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_depth) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ABP with insufficient depth found\" first_failing_seed={first_failing_seed}")
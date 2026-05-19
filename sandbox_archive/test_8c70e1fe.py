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
    
    n = 40
    target_value = 1 if sum(random.randint(0, 1) for _ in range(n)) % 2 == 1 else 0
    
    def depth(abp):
        if isinstance(abp, tuple):
            return max(depth(subtree) for subtree in abp)
        return 1
    
    def eval_abp(abp, n):
        if isinstance(abp, tuple):
            op = abp[0]
            left, right = abp[1], abp[2]
            if op == '+':
                return eval_abp(left, n) + eval_abp(right, n)
            elif op == '*':
                return eval_abp(left, n) * eval_abp(right, n)
            elif op == 'x':
                return n
        else:
            return abp
    
    min_depth = math.ceil(math.log2(n))
    
    def generate_abps():
        if n == 1:
            yield (n,)
        else:
            for left in generate_abps():
                for right in generate_abps():
                    yield ('+', left, right)
                    yield ('*', left, right)
    
    abps = list(generate_abps())
    random.shuffle(abps)
    abps = abps[:100]  # Limit to a manageable number of ABPs
    
    instances_tested = len(abps)
    conjecture_holds = True
    counterexample = ""
    
    for abp in abps:
        if depth(abp) < min_depth and eval_abp(abp, n) == target_value:
            continue
        else:
            conjecture_holds = False
            counterexample = f"ABP {abp} does not meet the depth requirement"
            break
    
    return {
        "metric_name": "depth",
        "metric_value": min_depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_depth = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_depth)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
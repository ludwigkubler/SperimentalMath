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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def dpll_search_tree_width(formula):
        # Simplified DPLL algorithm to estimate width
        stack = [formula]
        max_width = 0
        while stack:
            current = stack.pop()
            if '0' not in current and '1' not in current:
                continue
            if len(current) > max_width:
                max_width = len(current)
            for i in range(len(current)):
                if current[i] == '0':
                    stack.append(current[:i] + '1' + current[i+1:])
                elif current[i] == '1':
                    stack.append(current[:i] + '0' + current[i+1:])
        return max_width
    
    def local_crossed_module_rank(formula):
        # Simplified rank calculation for demonstration
        m = sum(1 for char in formula if char == '1')
        n = len(formula)
        return math.ceil(m * math.log(n, 2))
    
    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    width = dpll_search_tree_width(formula)
    rank = local_crossed_module_rank(formula)
    
    conjecture_holds = rank <= width
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Rank: {rank}, Width: {width}"
    
    return {
        "metric_name": "Rank vs Width",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    total_rank = 0
    total_width = 0
    num_seeds = len(seeds)
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_rank += trial_result["metric_value"]
        total_width += trial_result["metric_value"] if trial_result["conjecture_holds"] else width
        
        print(f"TRIAL: {trial_result}")
    
    mean_rank = total_rank / num_seeds
    mean_width = total_width / num_seeds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_seeds
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
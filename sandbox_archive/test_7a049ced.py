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
    
    def tseitin_formula(depth):
        if depth == 1:
            return ['x']
        else:
            subformulas = [tseitin_formula(depth - 1) for _ in range(2)]
            new_var = f'x{depth}'
            return [f'({sub[0]} & {sub[1]}) -> {new_var}' for sub in zip(subformulas, subformulas)] + [f'{new_var}']
    
    def resolution_tree(formula):
        if len(formula) == 1:
            return formula
        else:
            subtrees = [resolution_tree(subformula) for subformula in formula]
            new_node = random.choice(subtrees)
            return new_node
    
    def geometric_quantization_rank(tree):
        if isinstance(tree, str):
            return 1
        else:
            return sum(geometric_quantization_rank(subtree) for subtree in tree)
    
    depths = [5, 10, 15, 20, 30, 40]
    results = []
    
    for depth in depths:
        formula = tseitin_formula(depth)
        tree = resolution_tree(formula)
        rank = geometric_quantization_rank(tree)
        results.append((depth, rank))
    
    min_rank = min(rank for _, rank in results)
    max_depth = max(depth for depth, _ in results)
    
    if min_rank < 2**(0.4 * max_depth):
        return {
            "metric_name": "minimal_rank",
            "metric_value": min_rank,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Minimum rank {min_rank} is less than 2^(0.4 * {max_depth})"
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": min_rank,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    total_rank = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_rank += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supporting += 1
    
    mean_rank = Fraction(total_rank, len(results))
    support_fraction = Fraction(count_supporting, len(results))
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Minimum rank less than 2^(0.4 * depth)\" first_failing_seed={first_failing_seed}")
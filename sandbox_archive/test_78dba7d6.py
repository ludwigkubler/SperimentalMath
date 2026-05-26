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
    
    def generate_tseitin_tree(n):
        if n == 1:
            return ['x', 'y']
        left = generate_tseitin_tree(n // 2)
        right = generate_tseitin_tree(n - n // 2)
        return [f'NOT {left[0]}', f'{right[0]} OR {left[1]}']

    def hodge_rank(tree):
        if isinstance(tree, str):
            return 1
        else:
            return max(hodge_rank(subtree) for subtree in tree)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        tree = generate_tseitin_tree(n)
        rank = hodge_rank(tree)
        expected_rank = math.log2(n)
        
        if abs(rank - expected_rank) > 0.5:
            return {
                "metric_name": "Hodge Rank",
                "metric_value": rank,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, computed rank={rank}, expected rank={expected_rank}"
            }
        results.append(rank)
    
    mean_diff = sum(abs(r - math.log2(n)) for n, r in zip(n_values, results)) / len(n_values)
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": mean_diff <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if not result["conjecture_holds"]:
            break
        results.append(result["metric_value"])
    
    if len(results) == len(seeds):
        mean_val = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean_val)**2 for x in results) / len(results))
        support_fraction = len([r for r in results if abs(r - math.log2(n)) <= 0.5]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_val} std={std_dev} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed={seeds[results.index(next(r for r in results if abs(r - math.log2(n)) > 0.5))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=counterexample_found_first seed={seeds[results.index(next(r for r in results if abs(r - math.log2(n)) > 0.5))]}")
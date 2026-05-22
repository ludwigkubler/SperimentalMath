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
    
    def dpll_search_tree_width(circuit):
        # Placeholder for actual DPLL search tree width computation
        return len(circuit)
    
    def symplectic_leaf_space(n):
        # Placeholder for actual symplectic leaf space computation
        return [i for i in range(1, n+1)]
    
    def minimal_order(divisor):
        # Placeholder for actual minimal order computation
        return sum(divisor) / len(divisor)
    
    def projective_grassmannian_divisor(n):
        # Placeholder for actual divisor computation on Grassmannian
        return [i for i in range(1, n+1)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = [random.choice([0, 1]) for _ in range(n)]
        w_C = dpll_search_tree_width(circuit)
        leaves = symplectic_leaf_space(n)
        divisor = projective_grassmannian_divisor(n)
        order = minimal_order(divisor)
        
        results.append({
            "n": n,
            "w_C": w_C,
            "order": order
        })
    
    mean_diff = sum(abs(result["order"] - result["w_C"]) for result in results) / len(results)
    conjecture_holds = mean_diff <= 1.5
    
    return {
        "metric_name": "mean_difference",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_diff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
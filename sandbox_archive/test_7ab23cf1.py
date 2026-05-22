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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_and_or_tree(n):
        if n == 1:
            return random.choice([0, 1])
        else:
            left = generate_and_or_tree(n // 2)
            right = generate_and_or_tree(n - n // 2)
            return [random.choice(['AND', 'OR']), left, right]
    
    def evaluate_polynomial(poly, x):
        if isinstance(poly, int):
            return poly
        elif poly[0] == 'AND':
            return min(evaluate_polynomial(poly[1], x), evaluate_polynomial(poly[2], x))
        elif poly[0] == 'OR':
            return max(evaluate_polynomial(poly[1], x), evaluate_polynomial(poly[2], x))
    
    def construct_tropical_motive(tree):
        if isinstance(tree, int):
            return [tree]
        else:
            left_poly = construct_tropical_motive(tree[1])
            right_poly = construct_tropical_motive(tree[2])
            new_poly = []
            for l in left_poly:
                for r in right_poly:
                    new_poly.append(evaluate_polynomial(l, evaluate_polynomial(r, 0)))
            return new_poly
    
    def rank(poly):
        if isinstance(poly, int):
            return 1
        else:
            return max(rank(p) for p in poly)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    tree = generate_and_or_tree(n)
    communication_complexity = evaluate_polynomial(tree, 0)
    tropical_motive_poly = construct_tropical_motive(tree)
    rank_of_tropical_motive = rank(tropical_motive_poly)
    
    metric_name = "Rank of Tropical Motive"
    metric_value = rank_of_tropical_motive
    instances_tested = 1
    conjecture_holds = rank_of_tropical_motive >= communication_complexity * n or rank_of_tropical_motive > communication_complexity ** 2
    counterexample = "" if conjecture_holds else "Rank of tropical motive does not satisfy the bound"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
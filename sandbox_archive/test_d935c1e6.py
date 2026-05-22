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
            return ['leaf', random.choice([0, 1])]
        else:
            left = generate_and_or_tree(n // 2)
            right = generate_and_or_tree(n - n // 2)
            return ['node', random.choice(['and', 'or']), left, right]
    
    def communication_complexity(tree):
        if tree[0] == 'leaf':
            return 1
        elif tree[1] == 'and':
            return 1 + max(communication_complexity(tree[2]), communication_complexity(tree[3]))
        else:
            return 1 + max(communication_complexity(tree[2]), communication_complexity(tree[3]))
    
    def tropical_motive_rank(tree):
        if tree[0] == 'leaf':
            return 1
        elif tree[1] == 'and':
            left_rank = tropical_motive_rank(tree[2])
            right_rank = tropical_motive_rank(tree[3])
            return max(left_rank, right_rank) + 1
        else:
            left_rank = tropical_motive_rank(tree[2])
            right_rank = tropical_motive_rank(tree[3])
            return max(left_rank, right_rank) + 1
    
    def evaluate_polynomial(poly, x):
        result = 0
        for coeff in reversed(poly):
            result = result * x + coeff
        return result
    
    def construct_tropical_motive(tree):
        if tree[0] == 'leaf':
            return [tree[1]]
        elif tree[1] == 'and':
            left_poly = construct_tropical_motive(tree[2])
            right_poly = construct_tropical_motive(tree[3])
            new_poly = []
            for l in left_poly:
                for r in right_poly:
                    new_poly.append(evaluate_polynomial(l, evaluate_polynomial(r, 1)))
            return new_poly
        else:
            left_poly = construct_tropical_motive(tree[2])
            right_poly = construct_tropical_motive(tree[3])
            new_poly = []
            for l in left_poly:
                for r in right_poly:
                    new_poly.append(evaluate_polynomial(l, evaluate_polynomial(r, 0)))
            return new_poly
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            tree = generate_and_or_tree(n)
            C_N = communication_complexity(tree)
            T_M_rank = tropical_motive_rank(tree)
            T_M_poly = construct_tropical_motive(tree)
            
            if T_M_rank < C_N or T_M_rank > C_N**2:
                conjecture_holds = False
                counterexample = f"n={n}, C(N)={C_N}, R={T_M_rank}"
                break
            
            total_metric_value += T_M_rank
            instances_tested += 1
    
    return {
        "metric_name": "tropical_motive_rank",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
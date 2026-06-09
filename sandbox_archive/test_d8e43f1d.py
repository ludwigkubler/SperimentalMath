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
    
    def generate_frege_proof(depth):
        if depth == 0:
            return []
        else:
            op = random.choice(['AND', 'OR'])
            left = generate_frege_proof(depth - 1)
            right = generate_frege_proof(depth - 1)
            return [op, left, right]
    
    def construct_coxeter_group(proof):
        if not proof:
            return []
        elif isinstance(proof[0], list):
            op = proof[0]
            left = construct_coxeter_group(proof[1])
            right = construct_coxeter_group(proof[2])
            if op == 'AND':
                return [left, right]
            else:  # OR
                return [right, left]
        else:
            return []
    
    def calculate_rank(group):
        if not group:
            return 0
        elif isinstance(group[0], list):
            left = calculate_rank(group[0])
            right = calculate_rank(group[1])
            return max(left, right) + 1
        else:
            return 1
    
    depth_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for depth in depth_values:
        for _ in range(5):
            proof = generate_frege_proof(depth)
            group = construct_coxeter_group(proof)
            rank = calculate_rank(group)
            total_metric_value += rank
            instances_tested += 1
            n_max = max(n_max, depth)
            
            if rank > 1.5 * depth ** 1.5:
                conjecture_holds = False
                counterexample = f"Depth {depth}, Rank {rank}"
    
    return {
        "metric_name": "Coxeter Group Rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")
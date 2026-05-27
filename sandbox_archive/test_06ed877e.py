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
    
    def generate_random_boolean_function(n, depth):
        if depth == 0:
            return random.choice([0, 1])
        else:
            op = random.choice(['&', '|'])
            args = [generate_random_boolean_function(n, depth - 1) for _ in range(2)]
            return (op, args)
    
    def evaluate_boolean_function(f):
        if isinstance(f, int):
            return f
        elif isinstance(f, tuple):
            op, args = f
            if op == '&':
                return evaluate_boolean_function(args[0]) & evaluate_boolean_function(args[1])
            elif op == '|':
                return evaluate_boolean_function(args[0]) | evaluate_boolean_function(args[1])
    
    def tropicalize_boolean_function(f):
        if isinstance(f, int):
            return f
        elif isinstance(f, tuple):
            op, args = f
            if op == '&':
                return min(tropicalize_boolean_function(args[0]), tropicalize_boolean_function(args[1]))
            elif op == '|':
                return max(tropicalize_boolean_function(args[0]), tropicalize_boolean_function(args[1]))
    
    def rank_tropicalized_function(f):
        if isinstance(f, int):
            return 1
        elif isinstance(f, tuple):
            left_rank = rank_tropicalized_function(f[1][0])
            right_rank = rank_tropicalized_function(f[1][1])
            return max(left_rank, right_rank) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            depth = random.randint(1, n)
            f = generate_random_boolean_function(n, depth)
            tropicalized_f = tropicalize_boolean_function(f)
            rank = rank_tropicalized_function(tropicalized_f)
            total_metric_value += rank
            instances_tested += 1
            
            if rank < math.ceil(depth * math.log2(n)):
                conjecture_holds = False
                counterexample = f"n={n}, depth={depth}, rank={rank}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
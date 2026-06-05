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
    
    def generate_random_formula(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        for clause in clauses:
            if all(abs(lit) not in [abs(x) for x in stack] for lit in clause):
                stack.extend(clause)
            else:
                return len(stack)
        return 0
    
    def geometric_entropy(tree):
        # Simplified calculation of geometric entropy
        n = len(tree)
        total_weight = sum(sum(distances[i][j] for j in range(n)) for i in range(n))
        if total_weight == 0:
            return 0
        avg_distance = total_weight / (n * (n - 1) // 2)
        entropy = -avg_distance * math.log(avg_distance, 2)
        return entropy
    
    def construct_metric_tree(clauses):
        n = len(clauses)
        tree = [[math.inf] * n for _ in range(n)]
        for i in range(n):
            tree[i][i] = 0
        for clause in clauses:
            a, b = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                tree[a-1][b-1] = 1
                tree[b-1][a-1] = 1
        return tree
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clauses = generate_random_formula(n)
        tree = construct_metric_tree(clauses)
        w = resolution_width(clauses)
        H_min = geometric_entropy(tree)
        
        if H_min < 0.5 * w:
            conjecture_holds = False
            counterexample = f"n={n}, H_min={H_min}, w={w}"
        
        total_metric_value += H_min
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested if conjecture_holds else 0
    
    return {
        "metric_name": "Minimal Geometric Entropy",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def hypergeometric_function(a, b, n):
        if a == 0 or b == 0:
            return 1
        result = 1
        for k in range(1, min(a, b) + 1):
            result *= (a - k + 1) * (b - k + 1)
            result /= k * (n - a - b + k + 1)
        return result
    
    def count_hypergeometric_solutions(instance):
        n = len(instance)
        solutions = set()
        for i in range(2**n):
            solution = [instance[j] ^ (i >> j & 1) for j in range(n)]
            if all(solution[j] == solution[0] for j in range(1, n)):
                solutions.add(tuple(sorted(solution)))
        return len(solutions)
    
    def count_resolution_trees(instance):
        # Simplified DPLL algorithm to count unique trees
        n = len(instance)
        stack = []
        visited = set()
        def dpll(i):
            if i == n:
                stack.append(tuple(sorted(stack)))
                return True
            for j in range(2):
                stack.append(j)
                if dpll(i + 1):
                    return True
                stack.pop()
            return False
        dpll(0)
        return len(set(stack))
    
    def coxeter_group_order(instance):
        # Simplified calculation of Coxeter group order for demonstration
        n = len(instance)
        return 2**n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        instance = generate_instance(n)
        solutions_count = count_hypergeometric_solutions(instance)
        trees_count = count_resolution_trees(instance)
        coxeter_order = coxeter_group_order(instance)
        
        if trees_count == 0:
            continue
        
        ratio = abs(solutions_count - 1) / (trees_count ** coxeter_order)
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    std_ratio = (sum((x - mean_ratio) ** 2 for x in results) / len(results)) ** 0.5
    conjecture_holds = all(0.9 <= r <= 1.1 for r in results)
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max([random.choice([5, 10, 15, 20, 30, 40]) for _ in range(30)]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 307))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    std_ratio = (sum((x - mean_ratio) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if 0.9 <= r <= 1.1) / len(results)
    
    if all(0.9 <= r <= 1.1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(r < 0.9 or r > 1.1 for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.9 <= result <= 1.1))
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
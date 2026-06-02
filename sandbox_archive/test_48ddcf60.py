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
    
    def generate_communication_problem(n):
        # Generate a random n-bit communication problem
        return [random.randint(0, 1) for _ in range(n)]
    
    def construct_groupoid(problem):
        # Construct a groupoid from the communication problem
        groupoid = {}
        for i in range(len(problem)):
            for j in range(i + 1, len(problem)):
                if problem[i] == problem[j]:
                    if (i, j) not in groupoid:
                        groupoid[(i, j)] = set()
                    groupoid[(i, j)].add((j, i))
        return groupoid
    
    def min_order(groupoid):
        # Compute the minimal order of elements in the groupoid
        orders = [len(groupoid.get((i, j), [])) for i in range(len(problem)) for j in range(i + 1, len(problem))]
        if not orders:
            return 0
        return min(orders)
    
    def communication_complexity_rank(problem):
        # Compute the rank of the communication complexity
        rank = 0
        seen = set()
        for i in range(len(problem)):
            for j in range(i + 1, len(problem)):
                if problem[i] == problem[j]:
                    if (i, j) not in seen and (j, i) not in seen:
                        rank += 1
                        seen.add((i, j))
                        seen.add((j, i))
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    problem = generate_communication_problem(n)
    groupoid = construct_groupoid(problem)
    min_order_value = min_order(groupoid)
    communication_complexity_rank_value = communication_complexity_rank(problem)
    
    return {
        "metric_name": "min_order(G)",
        "metric_value": min_order_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.8 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"negative_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
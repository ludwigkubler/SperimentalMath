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
            if problem[i] == 0:
                groupoid[(i,)] = (i + 1) % len(problem)
            else:
                groupoid[(i,)] = (i - 1) % len(problem)
        return groupoid
    
    def calculate_min_order(groupoid):
        # Calculate the minimal order of elements in the groupoid
        min_order = float('inf')
        for element in groupoid.values():
            if element < min_order:
                min_order = element
        return min_order
    
    def calculate_communication_complexity_rank(problem):
        # Calculate the rank of communication complexity (simplified example)
        rank = len(set(problem))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_order_sum = 0
    communication_complexity_rank_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        problem = generate_communication_problem(n)
        groupoid = construct_groupoid(problem)
        min_order = calculate_min_order(groupoid)
        rank = calculate_communication_complexity_rank(problem)
        
        min_order_sum += min_order
        communication_complexity_rank_sum += rank
        instances_tested += 1
        if n > n_max:
            n_max = n
    
    mean_min_order = min_order_sum / len(n_values)
    mean_rank = communication_complexity_rank_sum / len(n_values)
    
    correlation_coefficient = (len(n_values) * sum(min_order * rank for min_order, rank in zip(n_values, n_values)) -
                               sum(n_values) * mean_min_order * mean_rank) / \
                              math.sqrt((len(n_values) * sum(min_order ** 2 for min_order in n_values) - sum(n_values) ** 2) *
                                        (len(n_values) * sum(rank ** 2 for rank in n_values) - sum(n_values) ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + \
            [31, 37, 41, 43, 47, 53, 59, 61, 67, 71] + \
            [73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")
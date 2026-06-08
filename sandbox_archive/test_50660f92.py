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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def truth_table_to_metric_space(truth_table):
        n = int(math.log2(len(truth_table)))
        metric_space = []
        for i in range(len(truth_table)):
            for j in range(i + 1, len(truth_table)):
                distance = sum(abs(a - b) for a, b in zip(truth_table[i], truth_table[j]))
                metric_space.append((i, j, distance))
        return metric_space
    
    def euclidean_distance(p1, p2):
        return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))
    
    def hyperbolic_distance(p1, p2):
        d_euclidean = euclidean_distance(p1, p2)
        if d_euclidean == 0:
            return 0
        return math.log((1 + d_euclidean) / (1 - d_euclidean))
    
    def max_hyperbolic_distance(metric_space):
        n = int(math.sqrt(len(metric_space)))
        points = [(i // n, i % n) for i in range(n**2)]
        max_dist = 0
        for p1, p2, _ in metric_space:
            dist = hyperbolic_distance(points[p1], points[p2])
            if dist > max_dist:
                max_dist = dist
        return max_dist
    
    def communication_complexity(truth_table):
        n = int(math.log2(len(truth_table)))
        instances_tested = 0
        total_bits_sent = 0
        for i in range(2**n):
            instance = [int(x) for x in format(i, f'0{n}b')]
            output = truth_table[i]
            bits_sent = sum(output.count(bit) for bit in set(output))
            instances_tested += 1
            total_bits_sent += bits_sent
        return total_bits_sent / instances_tested
    
    n_values = [5, 10, 15, 20, 30, 40]
    max_dist_sum = 0
    comm_complexity_sum = 0
    instances_tested_total = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            truth_table = generate_boolean_function(n)
            metric_space = truth_table_to_metric_space(truth_table)
            max_dist = max_hyperbolic_distance(metric_space)
            comm_complexity = communication_complexity(truth_table)
            max_dist_sum += max_dist
            comm_complexity_sum += comm_complexity
            instances_tested_total += 1
            n_max = max(n_max, n)
    
    if comm_complexity_sum == 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": instances_tested_total,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "communication_complexity_zero"
        }
    
    ratio = max_dist_sum / comm_complexity_sum
    return {
        "metric_name": "communication_complexity",
        "metric_value": ratio,
        "instances_tested": instances_tested_total,
        "n_max": n_max,
        "conjecture_holds": ratio >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='ratio_not_sufficiently_high' first_failing_seed={first_failing_seed}")
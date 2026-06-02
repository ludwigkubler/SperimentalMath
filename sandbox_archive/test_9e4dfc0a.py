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
    
    def generate_protocol_instances(n):
        protocols = []
        for _ in range(30):  # Ensure at least 30 instances per seed
            rank = random.randint(1, 5)  # Varying ranks from 1 to 5
            protocol = {
                'rank': rank,
                'input_size': n
            }
            protocols.append(protocol)
        return protocols
    
    def construct_lattice(protocol):
        rank = protocol['rank']
        input_size = protocol['input_size']
        lattice_points = []
        for i in range(input_size):
            for j in range(rank):
                lattice_points.append((i, j))
        return lattice_points
    
    def count_lattice_points(lattice_points):
        return len(lattice_points)
    
    def measure_rank(protocol):
        return protocol['rank']
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_points = 0
    total_ranks = 0
    
    for n in n_values:
        protocols = generate_protocol_instances(n)
        for protocol in protocols:
            lattice_points = construct_lattice(protocol)
            points_count = count_lattice_points(lattice_points)
            rank = measure_rank(protocol)
            total_points += points_count
            total_ranks += rank ** 2
    
    if total_ranks == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 180,  # 30 instances per n * 6 values of n
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_points = total_points / 180
    mean_ranks_squared = total_ranks / 180
    
    # Calculate Pearson correlation coefficient
    numerator = sum((points_count - mean_points) * (rank ** 2 - mean_ranks_squared)
                   for points_count, rank in zip([count_lattice_points(construct_lattice(protocol))
                                                  for protocol in generate_protocol_instances(40)],
                                                 [measure_rank(protocol) for protocol in generate_protocol_instances(40)]))
    denominator = math.sqrt(sum((points_count - mean_points) ** 2
                                for points_count in [count_lattice_points(construct_lattice(protocol))
                                                   for protocol in generate_protocol_instances(40)])) * \
                           math.sqrt(sum((rank ** 2 - mean_ranks_squared) ** 2
                                          for rank in [measure_rank(protocol) for protocol in generate_protocol_instances(40)]))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 180,  # 30 instances per n * 6 values of n
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 180,  # 30 instances per n * 6 values of n
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results if r['metric_value'] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
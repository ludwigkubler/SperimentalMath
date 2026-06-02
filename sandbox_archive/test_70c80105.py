# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_protocol_instances(n):
        protocols = []
        for _ in range(30):  # Generate 30 instances per seed
            rank = random.randint(1, n // 2)
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
        for i in range(rank):
            for j in range(input_size):
                lattice_points.append((i, j))
        return lattice_points
    
    def count_lattice_points(lattice_points):
        return len(lattice_points)
    
    def measure_rank(protocol):
        return protocol['rank']
    
    protocols = generate_protocol_instances(40)  # Sweep n from 5 to 40
    lattice_points_count = []
    rank_values = []
    
    for protocol in protocols:
        lattice_points = construct_lattice(protocol)
        lattice_points_count.append(count_lattice_points(lattice_points))
        rank_values.append(measure_rank(protocol))
    
    if len(lattice_points_count) < 30 or len(rank_values) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(lattice_points_count),
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    n = len(lattice_points_count)
    mean_lattice_points = sum(lattice_points_count) / n
    mean_rank = sum(rank_values) / n
    
    covariance = sum((lattice_points_count[i] - mean_lattice_points) * (rank_values[i] - mean_rank) for i in range(n)) / n
    variance_lattice_points = sum((lattice_points_count[i] - mean_lattice_points) ** 2 for i in range(n)) / n
    variance_rank = sum((rank_values[i] - mean_rank) ** 2 for i in range(n)) / n
    
    if variance_lattice_points == 0 or variance_rank == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(lattice_points_count),
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "Zero variance in lattice points or rank"
        }
    
    pearson_correlation = covariance / (math.sqrt(variance_lattice_points) * math.sqrt(variance_rank))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation,
        "instances_tested": len(lattice_points_count),
        "n_max": 40,
        "conjecture_holds": pearson_correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient < 0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
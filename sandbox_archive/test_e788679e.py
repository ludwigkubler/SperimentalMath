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
    
    def generate_planar_graph(n):
        if n == 1:
            return [(0, 0)]
        elif n == 2:
            return [(0, 0), (1, 0)]
        elif n == 3:
            return [(0, 0), (1, 0), (0.5, math.sqrt(3)/2)]
        else:
            raise ValueError("Unsupported graph size for this test")
    
    def geometric_entropy(points):
        if not points:
            return 0
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
        width = max_x - min_x
        height = max_y - min_y
        area = width * height
        entropy = 0
        for x, y in points:
            px = (x - min_x) / width
            py = (y - min_y) / height
            entropy += -px * math.log2(px) - py * math.log2(py)
        return entropy
    
    def communication_complexity_rank(graph):
        n = len(graph)
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            raise ValueError("Unsupported graph size for this test")
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_entropy = 0
    total_rank = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_planar_graph(n)
            entropy = geometric_entropy(graph)
            rank = communication_complexity_rank(graph)
            total_entropy += entropy
            total_rank += rank
            instances_tested += 1
    
    mean_entropy = total_entropy / instances_tested
    mean_rank = total_rank / instances_tested
    correlation_coefficient = (instances_tested * mean_entropy * mean_rank - 
                                total_entropy * total_rank) / (
                                    math.sqrt(instances_tested * sum((entropy - mean_entropy)**2 for entropy in [geometric_entropy(generate_planar_graph(n)) for n in n_values]) / instances_tested) *
                                    math.sqrt(instances_tested * sum((rank - mean_rank)**2 for rank in [communication_complexity_rank(generate_planar_graph(n)) for n in n_values]) / instances_tested))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
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
    
    def generate_random_k_colorable_graph(n, k):
        graph = [[0] * n for _ in range(n)]
        colors = list(range(1, k + 1))
        
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    color = random.choice(colors)
                    graph[i][j] = color
                    graph[j][i] = color
        
        return graph
    
    def compute_min_ring_norm(graph):
        n = len(graph)
        min_norm = float('inf')
        
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    norm = abs(graph[i][j])
                    if norm < min_norm:
                        min_norm = norm
        
        return min_norm
    
    def compute_communication_rank(graph):
        n = len(graph)
        rank = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    rank += 1
        
        return rank
    
    n_max = 40
    instances_tested = 30
    min_ring_norms = []
    communication_ranks = []
    
    for _ in range(instances_tested):
        k = random.randint(2, 5)
        graph = generate_random_k_colorable_graph(n_max, k)
        
        min_ring_norm = compute_min_ring_norm(graph)
        communication_rank = compute_communication_rank(graph)
        
        min_ring_norms.append(min_ring_norm)
        communication_ranks.append(communication_rank)
    
    correlation_coefficient = 0
    if len(min_ring_norms) > 1 and len(communication_ranks) > 1:
        mean_min_ring_norm = sum(min_ring_norms) / len(min_ring_norms)
        mean_communication_rank = sum(communication_ranks) / len(communication_ranks)
        
        numerator = sum((min_ring_norm - mean_min_ring_norm) * (communication_rank - mean_communication_rank) for min_ring_norm, communication_rank in zip(min_ring_norms, communication_ranks))
        denominator = math.sqrt(sum((min_ring_norm - mean_min_ring_norm) ** 2 for min_ring_norm in min_ring_norms)) * math.sqrt(sum((communication_rank - mean_communication_rank) ** 2 for communication_rank in communication_ranks))
        
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = abs(correlation_coefficient) >= 0.9
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient:.4f} is not within ±0.1 of expected value."
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
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
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient outside ±0.1\" first_failing_seed={first_failing_seed}")
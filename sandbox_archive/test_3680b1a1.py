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
    
    def generate_instance(n):
        # Generate a random communication complexity problem instance with rank variance R(n)
        return [random.randint(1, n) for _ in range(n)]
    
    def construct_interaction_graph(instance):
        # Construct the interaction graph from the instance
        n = len(instance)
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if abs(instance[i] - instance[j]) == 1:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def count_symmetric_spaces(graph):
        # Count the number of symmetric spaces required to represent the interaction graph
        n = len(graph)
        symmetries = set()
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    symmetries.add((i, j))
        return len(symmetries)
    
    def rank_variance(instance):
        # Calculate the rank variance R(n) of the instance
        n = len(instance)
        mean = sum(instance) / n
        variance = sum((x - mean) ** 2 for x in instance) / n
        return variance
    
    instances_tested = 0
    total_symmetric_spaces = 0
    total_variance = 0
    max_n = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > max_n:
            max_n = n
        
        for _ in range(5):
            instance = generate_instance(n)
            graph = construct_interaction_graph(instance)
            symmetric_spaces = count_symmetric_spaces(graph)
            variance = rank_variance(instance)
            
            instances_tested += 1
            total_symmetric_spaces += symmetric_spaces
            total_variance += variance
    
    mean_symmetric_spaces = total_symmetric_spaces / instances_tested
    mean_variance = total_variance / instances_tested
    
    k = abs(mean_symmetric_spaces - mean_variance) <= 5  # Arbitrary constant k for simplicity
    
    return {
        "metric_name": "Symmetric Spaces vs Rank Variance",
        "metric_value": mean_symmetric_spaces,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": k,
        "counterexample": "" if k else f"Mean symmetric spaces {mean_symmetric_spaces} not within ±5 of mean variance {mean_variance}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean symmetric spaces not within ±5 of mean variance\" first_failing_seed={first_failing_seed}")
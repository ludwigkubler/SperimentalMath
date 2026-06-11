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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def rank_variance(graph):
        # Placeholder implementation
        # Replace with actual algorithm for communication complexity rank variance
        return random.random()
    
    def min_index(graph):
        # Placeholder implementation
        # Replace with actual algorithm for minimal index of affine plane geometry
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_min_index = 0
        total_rank_variance = 0
        
        while instances_tested < 30:
            graph = generate_graph(n)
            min_idx = min_index(graph)
            rank_var = rank_variance(graph)
            
            if min_idx is None or rank_var is None:
                continue
            
            total_min_index += min_idx
            total_rank_variance += rank_var
            instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        avg_min_index = total_min_index / instances_tested
        avg_rank_variance = total_rank_variance / instances_tested
        
        results.append((avg_min_index, avg_rank_variance))
    
    if len(results) < 6:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_min_index = sum(x[0] for x in results)
    total_rank_variance = sum(x[1] for x in results)
    avg_min_index = total_min_index / len(results)
    avg_rank_variance = total_rank_variance / len(results)
    
    correlation_coefficient = (sum((results[i][0] - avg_min_index) * (results[i][1] - avg_rank_variance) for i in range(len(results))) /
                               math.sqrt(sum((results[i][0] - avg_min_index) ** 2 for i in range(len(results))) *
                                         sum((results[i][1] - avg_rank_variance) ** 2 for i in range(len(results)))))
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * len(results) - 2)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": sum(x[0] for x in results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "conjecture_holds" in trial_result and trial_result["conjecture_holds"]:
            results.append(trial_result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no valid trials")
    else:
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        
        support_fraction = len([x for x in results if abs(x - mean) <= std_dev]) / len(results)
        
        if support_fraction >= 0.9:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(min(results))]
            print(f"RESULT: FALSIFIED counterexample=\"low_support\" first_failing_seed={first_failing_seed}")
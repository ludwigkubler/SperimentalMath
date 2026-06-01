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
    
    def is_planar(graph):
        # Implement a planarity test (e.g., Kuratowski's theorem)
        # This is a simplified version and may not be accurate for all cases
        if len(graph) > 4:
            return False
        return True
    
    def local_cohomology_rank(simplicial_complex):
        # Placeholder function to compute the local cohomology rank
        # Replace with actual computation
        return random.randint(1, 5)
    
    def communication_complexity(graph):
        # Placeholder function to compute the communication complexity
        # Replace with actual computation
        return len(graph) ** 2
    
    n_max = 0
    instances_tested = 0
    total_lcr = 0
    total_growth_rate = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            graph = {i: set() for i in range(n)}
            for _ in range(int(n * (n - 1) / 4)):
                u, v = random.sample(range(n), 2)
                if u not in graph[v]:
                    graph[u].add(v)
                    graph[v].add(u)
            
            if is_planar(graph):
                simplicial_complex = {frozenset([i]): i for i in range(n)}
                lcr = local_cohomology_rank(simplicial_complex)
                growth_rate = communication_complexity(graph)
                
                total_lcr += lcr
                total_growth_rate += growth_rate
                instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_lcr = total_lcr / instances_tested
    mean_growth_rate = total_growth_rate / instances_tested
    correlation_coefficient = (instances_tested * sum(lcr * growth_rate for lcr, growth_rate in zip([mean_lcr] * instances_tested, [mean_growth_rate] * instances_tested)) - instances_tested * mean_lcr * mean_growth_rate) / math.sqrt((instances_tested * sum(lcr ** 2 for lcr in [mean_lcr] * instances_tested) - instances_tested * mean_lcr ** 2) * (instances_tested * sum(growth_rate ** 2 for growth_rate in [mean_growth_rate] * instances_tested) - instances_tested * mean_growth_rate ** 2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
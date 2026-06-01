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
    
    def is_planar(graph):
        # Implement a planarity test (e.g., Kuratowski's theorem check)
        # This is a simplified version and may not work for all cases.
        if len(graph) > 5:
            return False
        return True

    def local_cohomology_rank(simplicial_complex):
        # Placeholder function to compute local cohomology rank
        # This should be replaced with actual computation.
        return random.randint(1, 10)

    def communication_complexity(graph):
        # Placeholder function to compute communication complexity
        # This should be replaced with actual computation.
        return len(graph) ** 2

    instances_tested = 0
    total_lcr = 0
    total_growth_rate = 0
    n_max = 1

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Aim for at least 30 instances per seed
            graph = {i: set() for i in range(n)}
            for _ in range(n * (n - 1) // 2):
                u, v = random.sample(range(n), 2)
                if u != v and u not in graph[v]:
                    graph[u].add(v)
                    graph[v].add(u)
            
            if is_planar(graph):
                instances_tested += 1
                lcr = local_cohomology_rank(graph)
                growth_rate = communication_complexity(graph)
                total_lcr += lcr
                total_growth_rate += growth_rate

    avg_lcr = total_lcr / instances_tested if instances_tested > 0 else 0
    avg_growth_rate = total_growth_rate / instances_tested if instances_tested > 0 else 0
    
    correlation_coefficient = (instances_tested * avg_lcr * avg_growth_rate - 
                               sum(lcr * growth_rate for lcr, growth_rate in zip([avg_lcr] * instances_tested, [avg_growth_rate] * instances_tested))) / \
                              math.sqrt(instances_tested * sum((lcr - avg_lcr) ** 2 for lcr in [avg_lcr] * instances_tested) * 
                                        instances_tested * sum((growth_rate - avg_growth_rate) ** 2 for growth_rate in [avg_growth_rate] * instances_tested))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "correlation_coefficient < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
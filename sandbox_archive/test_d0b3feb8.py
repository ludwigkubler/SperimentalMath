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
        # Implement planarity test (e.g., Kuratowski's theorem)
        pass
    
    def delauany_complex_rank(graph):
        # Implement Delaunay complex rank calculation
        pass
    
    def circuit_monotone_width(graph):
        # Implement circuit monotone width calculation
        pass
    
    n_max = 0
    instances_tested = 0
    total_rd = 0
    total_wm = 0
    valid_instances = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size with 5 instances
            if n_max >= n:
                continue
            
            graph = generate_random_planar_graph(n)
            if not is_planar(graph):
                continue
            
            rd = delauany_complex_rank(graph)
            wm = circuit_monotone_width(graph)
            
            if rd < 0 or wm < 0:
                continue
            
            total_rd += rd
            total_wm += wm
            instances_tested += 1
            n_max = max(n_max, n)
            
            if rd >= wm**2:
                valid_instances += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    correlation_coefficient = total_rd / (instances_tested * total_wm)
    conjecture_holds = correlation_coefficient >= 0.8 and valid_instances == instances_tested
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
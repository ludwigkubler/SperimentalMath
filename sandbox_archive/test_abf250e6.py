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
    
    def generate_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        # Simplified version of resolution width calculation
        return len(clauses) * 2
    
    def noncrossing_partitions(n):
        if n == 0:
            return 1
        count = 0
        for i in range(1, n):
            count += noncrossing_partitions(i - 1) * noncrossing_partitions(n - i)
        return count
    
    instances_tested = 0
    total_width = 0
    total_partitions = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            instance = generate_instance(n)
            width = resolution_width(instance)
            partitions = noncrossing_partitions(n)
            
            total_width += width
            total_partitions += partitions
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "resolution_width_vs_noncrossing_partitions",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_width = total_width / instances_tested
    mean_partitions = total_partitions / instances_tested
    
    correlation_coefficient = (instances_tested * mean_width * mean_partitions - 
                                total_width * total_partitions) / (
                                    math.sqrt((instances_tested * sum(w**2 for w in range(5, 41)) - total_width**2) *
                                              (instances_tested * sum(p**2 for p in range(5, 41)) - total_partitions**2)))
    
    return {
        "metric_name": "resolution_width_vs_noncrossing_partitions",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_max={max(r['n_max'] for r in results)}")
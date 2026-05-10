# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_disjointness_instance(n):
    points = list(range(1, 2**n))
    lines = []
    for i in range(n):
        line = [j for j in points if (j & (1 << i)) != 0]
        lines.append(line)
    return points, lines

def compute_min_incidence(points, lines):
    incidence_matrix = [[0] * len(lines) for _ in range(len(points))]
    for i, point in enumerate(points):
        for j, line in enumerate(lines):
            if any(point & (1 << k) != 0 for k in line):
                incidence_matrix[i][j] = 1
    min_incidence = min(sum(row) for row in incidence_matrix)
    return min_incidence

def compute_communication_complexity(points, lines):
    n = len(points)
    communication_matrix = [[0] * n for _ in range(n)]
    for i, point in enumerate(points):
        for j, point2 in enumerate(points):
            if any(point & (1 << k) != 0 for k in points[j]):
                communication_matrix[i][j] = 1
    # Simplified version of communication complexity calculation
    return sum(sum(row) for row in communication_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        points, lines = generate_disjointness_instance(n)
        min_incidence = compute_min_incidence(points, lines)
        comm_complexity = compute_communication_complexity(points, lines)
        
        if min_incidence == 0:
            return {
                "metric_name": "min_incidence",
                "metric_value": None,
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": "min_incidence_zero"
            }
        
        log_comm_complexity = math.log(comm_complexity)
        conjecture_holds = abs(log_comm_complexity - (1 / min_incidence)) < 0.1
        
        results.append({
            "n": n,
            "min_incidence": min_incidence,
            "comm_complexity": comm_complexity,
            "log_comm_complexity": log_comm_complexity,
            "conjecture_holds": conjecture_holds
        })
    
    return {
        "metric_name": "min_incidence",
        "metric_value": sum(result["min_incidence"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 200, 7))
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        all_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in all_results if r["metric_value"] is not None) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in all_results if r["metric_value"] is not None) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_incidence_zero\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
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
    
    def generate_disjointness_instance(n):
        points = [(random.random(), random.random()) for _ in range(2 * n)]
        disjoint = [False] * (n * (n - 1) // 2)
        for i in range(n):
            for j in range(i + 1, n):
                if abs(points[2 * i][0] - points[2 * j][0]) > 0.5 or abs(points[2 * i][1] - points[2 * j][1]) > 0.5:
                    disjoint[i * (n - 1) // 2 + j - 1] = True
        return points, disjoint
    
    def communication_complexity(points, disjoint):
        n = len(points) // 2
        cc = 0
        for i in range(n):
            for j in range(i + 1, n):
                if disjoint[i * (n - 1) // 2 + j - 1]:
                    cc += math.log2(n)
        return cc
    
    def minimal_rank(points):
        # Placeholder function to compute the minimal rank of a manifold
        # This is a dummy implementation and should be replaced with actual geometric group theory code
        n = len(points) // 2
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        points, disjoint = generate_disjointness_instance(n)
        cc = communication_complexity(points, disjoint)
        rank = minimal_rank(points)
        
        if cc != math.log2(n):
            return {
                "metric_name": "communication_complexity",
                "metric_value": cc,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, CC={cc}, expected log({n})={math.log2(n)}"
            }
        
        results.append({
            "n": n,
            "communication_complexity": cc,
            "minimal_rank": rank
        })
    
    mean_cc = sum(result["communication_complexity"] for result in results) / len(results)
    std_cc = math.sqrt(sum((result["communication_complexity"] - mean_cc) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["minimal_rank"] <= result["n"]) / len(results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 35)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_cc = sum(result["metric_value"] for result in results) / len(results)
    std_cc = math.sqrt(sum((result["metric_value"] - mean_cc) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_cc} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['n']}, CC={result['metric_value']}, expected log({result['n']})={math.log2(result['n'])}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
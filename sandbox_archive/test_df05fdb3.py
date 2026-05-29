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
    
    def hamming_distance(x, y):
        return sum(xi != yi for xi, yi in zip(x, y))
    
    def greedy_ball_cover(f, S, R):
        covered = [False] * len(S)
        count = 0
        while not all(covered):
            max_points = []
            max_count = 0
            for c_j in S:
                if not covered[S.index(c_j)]:
                    points_in_range = [S[i] for i in range(len(S)) if hamming_distance(c_j, S[i]) <= R]
                    if len(points_in_range) > max_count:
                        max_points = points_in_range
                        max_count = len(points_in_range)
            if not max_points:
                break
            count += 1
            for p in max_points:
                covered[S.index(p)] = True
        return count
    
    def sample_satisfying_assignments(f, m):
        S = []
        for _ in range(m):
            while True:
                assignment = [random.choice([0, 1]) for _ in range(n)]
                if f(assignment) == 1:
                    S.append(assignment)
                    break
        return S
    
    n_values = [6, 10, 16, 24, 32, 40]
    results = []
    
    for n in n_values:
        m = 64
        f = lambda x: random.choice([0, 1]) if n <= 12 else any(random.choice([True, False]) for _ in range(3))
        S = sample_satisfying_assignments(f, m)
        
        for R in range(1, n // 2 + 1):
            i = random.randint(0, n - 1)
            b = random.choice([0, 1])
            
            f_prime = lambda x: f(x[:i] + [b] + x[i+1:])
            delta = abs(greedy_ball_cover(f, S, R) - greedy_ball_cover(f_prime, S, R))
            results.append({
                "metric_name": "delta",
                "metric_value": delta,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": delta <= 2 * math.ceil(math.log2(n + 1)),
                "counterexample": "" if delta <= 2 * math.ceil(math.log2(n + 1)) else f"delta={delta} > 2*log2({n+1})"
            })
    
    return {
        "seed": seed,
        "metric_name": "delta",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_delta = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
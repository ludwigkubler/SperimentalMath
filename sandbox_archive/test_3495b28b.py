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
    
    def hamming_distance(a, b):
        return sum(1 for x, y in zip(a, b) if x != y)
    
    def bit_packed_hamming(a, b):
        return bin(int(a, 2) ^ int(b, 2)).count('1')
    
    def greedy_ball_cover(f, S, R):
        covered = set()
        proxy_value = 0
        while len(covered) < len(S):
            max_points = []
            max_count = 0
            for c in S:
                if c not in covered:
                    count = sum(1 for s in S if bit_packed_hamming(c, s) <= R)
                    if count > max_count or (count == max_count and int(c, 2) < int(max_points[0], 2)):
                        max_points = [c]
                        max_count = count
            proxy_value += max_count
            for c in max_points:
                covered.add(c)
        return proxy_value - 1
    
    def sample_satisfying_assignments(f, m):
        if len(f) <= 64:
            return list(filter(lambda x: f(x), product([0, 1], repeat=len(f))))
        else:
            assignments = []
            for _ in range(m):
                assignment = ''.join(str(random.randint(0, 1)) for _ in range(len(f)))
                if f(assignment) == 1:
                    assignments.append(assignment)
                if len(assignments) >= m:
                    break
            return assignments
    
    def random_triple(n):
        i = random.randint(0, n - 1)
        b = random.choice([0, 1])
        R = random.randint(1, n // 2)
        return i, b, R
    
    n_values = [6, 10, 16, 24, 32, 40]
    m = 64
    results = []
    
    for n in n_values:
        f = ''.join(str(random.randint(0, 1)) for _ in range(n))
        S = sample_satisfying_assignments(f, m)
        
        for _ in range(30):
            i, b, R = random_triple(n)
            f_i_b = f[:i] + str(b) + f[i+1:]
            delta = abs(greedy_ball_cover(f, S, R) - greedy_ball_cover(f_i_b, S, R))
            results.append({
                "metric_name": "delta",
                "metric_value": delta,
                "instances_tested": 30,
                "n_max": n,
                "conjecture_holds": delta <= 2 * math.ceil(math.log2(n + 1)),
                "counterexample": ""
            })
    
    return {
        "seed": seed,
        "metric_name": "delta",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
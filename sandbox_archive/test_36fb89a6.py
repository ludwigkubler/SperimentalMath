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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_projective_plane(q):
    if not (q > 1 and is_prime(q)):
        raise ValueError("q must be a prime power")
    
    points = list(range(q**2 + q + 1))
    lines = []
    for i in range(q**2 + q + 1):
        line = [i]
        for j in range(1, q + 1):
            line.append((i + j * (q + 1)) % (q**2 + q + 1))
        lines.append(line)
    
    return points, lines

def incidence_matrix(points, lines):
    n = len(points)
    M = [[0] * n for _ in range(n)]
    for line in lines:
        for i in range(n):
            if i in line:
                for j in range(i + 1, n):
                    if j in line:
                        M[i][j] += 1
                        M[j][i] += 1
    return M

def discrepancy(M):
    n = len(M)
    max_discrepancy = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(sum(M[i]) - sum(M[j]))
            if d > max_discrepancy:
                max_discrepancy = d
    return max_discrepancy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    q_values = [2, 3, 4]
    results = []
    
    for q in q_values:
        try:
            points, lines = generate_projective_plane(q)
            M = incidence_matrix(points, lines)
            D = discrepancy(M)
            results.append(D)
        except ValueError as e:
            return {
                "metric_name": "discrepancy",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([D for D in results if abs(D - q**2) < 1e-6]) / len(results)
    
    return {
        "metric_name": "discrepancy",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"q={q_values[results.index(max(results))]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"q={result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
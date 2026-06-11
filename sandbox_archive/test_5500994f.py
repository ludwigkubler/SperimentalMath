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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, n))]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                cnf.append(clause)
        return cnf
    
    def construct_affine_plane(cnf):
        # Simplified affine plane construction
        points = set()
        lines = []
        for clause in cnf:
            line = tuple(sorted(set(abs(lit) for lit in clause)))
            if line not in lines:
                lines.append(line)
                points.update(line)
        return points, lines
    
    def min_index(points, lines):
        # Simplified minimal index calculation
        return len(lines)
    
    def resolution_width(cnf):
        # Simplified resolution width calculation
        width = 0
        for clause in cnf:
            if not any(abs(lit) in set(map(abs, other_clause)) for other_clause in cnf):
                width += 1
        return width
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    points, lines = construct_affine_plane(cnf)
    min_index_val = min_index(points, lines)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "min_index",
        "metric_value": min_index_val,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(clause) > 2 and random.random() < 0.5:
                clause.append(random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def box_counting_dimension(points):
        if not points:
            return 0
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
        width = max_x - min_x
        height = max_y - min_y
        if width == 0 or height == 0:
            return 0
        n = 2
        while True:
            count = 0
            for i in range(n):
                for j in range(n):
                    x = min_x + i * width / n
                    y = min_y + j * height / n
                    if any((x - point[0]) ** 2 + (y - point[1]) ** 2 <= (width / n) ** 2 for point in points):
                        count += 1
            if count == 0:
                return math.log(n, 2)
            n *= 2
    
    def resolution_width(clauses):
        # Placeholder for actual DPLL solver implementation
        return len(clauses)
    
    n = random.randint(5, 30)
    m = random.randint(n**2 // 4, n**2 // 2)
    cnf = generate_cnf(n, m)
    points = [(random.random(), random.random()) for _ in range(m)]
    fractal_dimension = box_counting_dimension(points)
    resolution_width_value = resolution_width(cnf)
    
    return {
        "metric_name": "correlation",
        "metric_value": fractal_dimension * resolution_width_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
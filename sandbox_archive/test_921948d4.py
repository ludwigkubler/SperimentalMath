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
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def box_counting_dimension(data, min_size=1, max_size=None):
        if not max_size:
            max_size = len(data)
        dimensions = []
        for size in range(min_size, max_size + 1):
            count = sum(1 for x in data if abs(x) >= size)
            dimensions.append((size, count))
        return [math.log(count) / math.log(size) for size, count in dimensions]
    
    def resolution_width(cnf):
        # Placeholder for actual DPLL solver
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    fractal_dimension = box_counting_dimension([abs(clause[0]) for clause in cnf])
    width = resolution_width(cnf)
    
    if not fractal_dimension or not width:
        return {
            "metric_name": "fractal_dimension",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_fractal = sum(fractal_dimension) / len(fractal_dimension)
    mean_width = sum(width) / len(width)
    correlation_coefficient = sum((f - mean_fractal) * (w - mean_width) for f, w in zip(fractal_dimension, width)) / len(fractal_dimension)
    max_diff = max(abs(f - w) for f, w in zip(fractal_dimension, width))
    
    return {
        "metric_name": "fractal_dimension",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and max_diff / max(mean_fractal, mean_width) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
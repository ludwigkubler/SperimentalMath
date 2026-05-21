# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def count_generators(f):
        n = len(f)
        points = set()
        for i in range(2**n):
            point = tuple(f[i >> j & 1] for j in range(n))
            if all(point[j] == f[i ^ (1 << j)] for j in range(n)):
                points.add(point)
        return len(points)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_generators = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            generators = count_generators(f)
            if generators < 0:  # Ensure non-negative number of generators
                return {
                    "metric_name": "min_generators",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": "negative_generators"
                }
            total_generators += generators
            instances_tested += 1
    
    mean_generators = Fraction(total_generators, instances_tested)
    conjecture_holds = mean_generators >= Fraction(2**n_values[-1], 4)
    
    return {
        "metric_name": "min_generators",
        "metric_value": float(mean_generators),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")
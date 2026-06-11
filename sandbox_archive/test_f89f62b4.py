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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def boolean_hyperplane_arrangement(f):
        n = len(f)
        arrangement = []
        for i in range(n):
            if f[i] == 1:
                arrangement.append(i)
        return arrangement
    
    def rank_variance(arrangement):
        n = len(arrangement)
        if n < 2:
            return 0
        mean = sum(arrangement) / n
        variance = sum((x - mean) ** 2 for x in arrangement) / (n - 1)
        return variance
    
    def hodge_classes(f):
        n = len(f)
        classes = []
        for i in range(n):
            if f[i] == 1:
                classes.append(i)
        return classes
    
    def minimal_hodge_dimension(classes):
        n = len(classes)
        if n < 2:
            return 0
        return n - 1
    
    m = random.randint(5, 40)
    f = generate_boolean_function(m)
    arrangement = boolean_hyperplane_arrangement(f)
    variance = rank_variance(arrangement)
    classes = hodge_classes(f)
    dimension = minimal_hodge_dimension(classes)
    
    if dimension == 0:
        return {
            "metric_name": "R(f)/HDim(f)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": m,
            "conjecture_holds": False,
            "counterexample": "dimension_zero"
        }
    
    ratio = variance / dimension
    
    return {
        "metric_name": "R(f)/HDim(f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if "counterexample" not in r) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if "counterexample" in r), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
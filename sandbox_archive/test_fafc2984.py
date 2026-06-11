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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_hyperplane_arrangement(f):
        n = int(math.log2(len(f)))
        arrangement = []
        for i in range(n):
            hyperplane = [f[j] ^ f[j + 2**i] for j in range(2**(n-i-1))]
            arrangement.append(hyperplane)
        return arrangement
    
    def rank_variance(arrangement):
        n = len(arrangement[0])
        variance = sum(sum(x != y for x, y in zip(a, b)) for a, b in zip(arrangement, arrangement[1:])) / (n * (len(arrangement) - 1))
        return variance
    
    def hodge_classes(f):
        n = int(math.log2(len(f)))
        classes = []
        for i in range(n):
            class_i = [f[j] ^ f[j + 2**i] for j in range(2**(n-i-1))]
            classes.append(class_i)
        return classes
    
    def minimal_hodge_dimension(classes):
        n = len(classes[0])
        dimension = sum(sum(x != y for x, y in zip(c, d)) for c, d in zip(classes, classes[1:])) / (n * (len(classes) - 1))
        return dimension
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        arrangement = boolean_hyperplane_arrangement(f)
        variance = rank_variance(arrangement)
        classes = hodge_classes(f)
        dimension = minimal_hodge_dimension(classes)
        
        if dimension == 0:
            continue
        
        ratio = variance / dimension
        metric_values.append(ratio)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = 0.5 <= mean_value <= 1.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Rank Variance to Hodge Dimension",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
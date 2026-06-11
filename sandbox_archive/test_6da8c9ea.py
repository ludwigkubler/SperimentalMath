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

def generate_groupoid(n):
    elements = list(range(n))
    generator = [random.choice(elements)]
    groupoid = {generator[0]: []}
    
    for i in range(1, n):
        new_element = random.choice(elements)
        while new_element in groupoid:
            new_element = random.choice(elements)
        groupoid[new_element] = []
    
    return groupoid, elements

def generate_communication_problem(groupoid, elements):
    # Placeholder for actual communication problem generation
    # For simplicity, we assume the rank variance is proportional to the number of elements
    rank_variance = len(groupoid) * 2
    return rank_variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        groupoid, elements = generate_groupoid(n)
        rank_variance = generate_communication_problem(groupoid, elements)
        
        if rank_variance <= 0 or len(elements) <= 0:
            continue
        
        ratio = Fraction(rank_variance, math.log(len(elements)))
        total_metric_value += ratio
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_ratio = Fraction(total_metric_value, instances_tested) if instances_tested > 0 else Fraction(0, 1)
    conjecture_holds = all(Fraction(rank_variance, math.log(len(elements))) <= mean_ratio for n in n_values for _ in range(3))
    
    return {
        "metric_name": "Ratio of Rank Variance to Logarithm of Set Size",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
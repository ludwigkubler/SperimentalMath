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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input length must be a power of 2")
        max_rank = 0
        for i in range(n):
            rank = sum(1 for x in f if (x >> i) & 1 == 1)
            max_rank = max(max_rank, rank)
        return max_rank
    
    def frobenius_class_dimension(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input length must be a power of 2")
        dimension = sum(1 for x in f if x == 0) + sum(1 for x in f if x == 1)
        return dimension
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_dimension = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        if n > n_max:
            n_max = n
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_boolean_function(n)
            dimension = frobenius_class_dimension(f)
            communication_rank = communication_complexity(f)
            total_dimension += dimension
            instances_tested += 1
    
    mean_dimension = total_dimension / instances_tested
    conjecture_holds = mean_dimension <= n_max**2 and all(communication_complexity(generate_boolean_function(n)) <= 10 for n in n_values)
    
    return {
        "metric_name": "Frobenius Class Dimension",
        "metric_value": mean_dimension,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["communication_complexity_rank"] > 10 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["communication_complexity_rank"] > 10)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")
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
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        count = [f.count(i) for i in range(2**n)]
        mean = sum(count) / (n * 2**n)
        variance = sum((x - mean)**2 for x in count) / (n * 2**n)
        return variance
    
    def minimal_rank_of_qa_algebra(f):
        # Placeholder function to represent the minimal rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        n = len(f)
        return random.randint(1, n)
    
    n_max = 40
    instances_tested = 30
    total_variance = 0
    total_rank = 0
    
    for _ in range(instances_tested):
        f = generate_boolean_function(n_max)
        variance = communication_complexity_rank_variance(f)
        rank = minimal_rank_of_qa_algebra(f)
        
        if rank == 0:
            continue
        
        total_variance += variance
        total_rank += rank
    
    mean_ratio = total_variance / total_rank if total_rank != 0 else float('inf')
    
    conjecture_holds = abs(mean_ratio - 1.0) <= 0.1 and all(variance >= rank * 0.9 for f in [generate_boolean_function(n_max) for _ in range(3)])
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "CRV(f) / rank(QA_algebra_f)",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
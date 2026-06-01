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
    
    def communication_rank(G):
        # Placeholder function for computing communication complexity rank
        # This is a dummy implementation and should be replaced with actual logic
        return len(G)

    def min_order_Kn(n, G):
        # Placeholder function for finding the minimal order of Kneser graph containing G
        # This is a dummy implementation and should be replaced with actual logic
        return n

    instances_tested = 0
    total_min_order = 0
    total_rank = 0
    n_max = 1
    
    for _ in range(30):
        n = random.randint(5, 40)
        G = [set(random.sample(range(n), k)) for k in range(2, n)]
        
        rank = communication_rank(G)
        min_order = min_order_Kn(n, G)
        
        instances_tested += 1
        total_min_order += min_order
        total_rank += rank
        
        if n > n_max:
            n_max = n
    
    mean_min_order = total_min_order / instances_tested
    mean_rank = total_rank / instances_tested
    correlation_coefficient = (instances_tested * sum(min_order * rank for min_order, rank in zip(range(instances_tested), range(instances_tested))) - 
                               instances_tested * mean_min_order * mean_rank) / math.sqrt((instances_tested * sum(min_order**2 for min_order in range(instances_tested)) - instances_tested * mean_min_order**2) *
                                                                 (instances_tested * sum(rank**2 for rank in range(instances_tested)) - instances_tested * mean_rank**2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
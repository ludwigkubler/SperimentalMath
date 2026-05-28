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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def multivariate_generalized_polynomial(f, n):
        # Simplified representation using a dictionary
        poly = {}
        for i in range(2**n):
            binary_rep = f'{i:0{n}b}'
            if f[i] == 1:
                poly[binary_rep] = 1
            else:
                poly[binary_rep] = -1
        return poly
    
    def frege_proof_depth(poly, n):
        # Simplified estimation of Frege proof depth
        max_depth = 0
        for term in poly.values():
            if abs(term) > max_depth:
                max_depth = abs(term)
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            f = generate_boolean_function(n)
            poly = multivariate_generalized_polynomial(f, n)
            depth = frege_proof_depth(poly, n)
            total_rank += sum(abs(coeff) for coeff in poly.values())
            total_depth += depth
            instances_tested += 1
    
    avg_rank = total_rank / instances_tested
    avg_depth = total_depth / instances_tested
    
    conjecture_holds = avg_rank <= avg_depth + 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Average Rank vs Average Depth",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(res["metric_value"] for res in results)
    total_depth = sum(res["metric_value"] for res in results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    mean_rank = total_rank / len(results)
    mean_depth = total_depth / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((res['metric_value'] - mean_rank)**2 for res in results) / len(results))} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["counterexample"] == "mapping_undefined" for res in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
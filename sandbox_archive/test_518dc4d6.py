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
        for _ in range(2**n // 3):  # Ensure at least one clause per literal
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            random.shuffle(literals)
            clauses.append(literals)
        return clauses
    
    def haversine_distance(p1, p2):
        R = 6371e3  # Earth's radius in meters
        lat1, lon1 = math.radians(p1[0]), math.radians(p1[1])
        lat2, lon2 = math.radians(p2[0]), math.radians(p2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    def hausdorff_distance(A, B):
        max_A_to_B = max(min(haversine_distance(p, q) for q in B) for p in A)
        max_B_to_A = max(min(haversine_distance(q, p) for p in A) for q in B)
        return max(max_A_to_B, max_B_to_A)
    
    def frege_proof_width(cnf):
        n = len(cnf[0])
        width = 1
        for clause in cnf:
            if len(set(abs(lit) for lit in clause)) > width:
                width = len(set(abs(lit) for lit in clause))
        return width
    
    def intrinsic_hausdorff_dimension(n):
        # Simplified approximation using a geometric progression
        return 2 * math.log(n) / math.log(2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            cnf = generate_cnf(n)
            width = frege_proof_width(cnf)
            D_H = intrinsic_hausdorff_dimension(n)
            total_metric_value += abs(width - (D_H**2 * n))
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Frege Proof Width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")
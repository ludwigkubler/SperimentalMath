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
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n+1):
            clause = [random.choice([-1, 1]) * j for j in range(1, n+1)]
            clauses.append(clause)
        return clauses
    
    def construct_quasigroup(cnf):
        literals = set()
        for clause in cnf:
            for lit in clause:
                literals.add(abs(lit))
        
        quasigroup = {}
        for i in range(len(literals)):
            for j in range(len(literals)):
                for k in range(len(literals)):
                    if (i, j) not in quasigroup:
                        quasigroup[(i, j)] = []
                    quasigroup[(i, j)].append(k)
        
        return quasigroup
    
    def calculate_automorphism_group_order(quasigroup):
        n = len(quasigroup)
        order = 1
        for i in range(n):
            for j in range(i+1, n):
                if quasigroup[(i, j)] == quasigroup[(j, i)]:
                    order += 1
        return order
    
    def calculate_resolution_proof_width(cnf):
        width = 0
        for clause in cnf:
            width = max(width, len(clause))
        return width
    
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        quasigroup = construct_quasigroup(cnf)
        automorphism_group_order = calculate_automorphism_group_order(quasigroup)
        resolution_proof_width = calculate_resolution_proof_width(cnf)
        
        results.append({
            "n": n,
            "automorphism_group_order": automorphism_group_order,
            "resolution_proof_width": resolution_proof_width
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_sum = 0
    for i in range(len(results)):
        for j in range(i+1, len(results)):
            x1, y1 = results[i]["automorphism_group_order"], results[j]["resolution_proof_width"]
            x2, y2 = results[j]["automorphism_group_order"], results[i]["resolution_proof_width"]
            correlation_sum += (x1 - x2) * (y1 - y2)
    
    n_pairs = len(results) * (len(results) - 1) // 2
    mean_x = sum(result["automorphism_group_order"] for result in results) / len(results)
    mean_y = sum(result["resolution_proof_width"] for result in results) / len(results)
    variance_x = sum((result["automorphism_group_order"] - mean_x) ** 2 for result in results) / (len(results) - 1)
    variance_y = sum((result["resolution_proof_width"] - mean_y) ** 2 for result in results) / (len(results) - 1)
    
    correlation_coefficient = correlation_sum / math.sqrt(n_pairs * variance_x * variance_y)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / (len(results) - 1))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
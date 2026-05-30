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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def cnf_to_polynomial(cnf):
        n = len(cnf)
        polynomial = 0
        for clause in cnf:
            term = 1
            for lit in clause:
                if lit > 0:
                    term *= (1 - x[lit])
                else:
                    term *= (1 + x[-lit])
            polynomial += term
        return polynomial
    
    def min_toric_variety(polynomial):
        # Simplified mapping to vertices count
        # This is a placeholder and should be replaced with actual computation
        return len(polynomial.split(' & ')) + len(polynomial.split(' | '))
    
    def circuit_complexity(cnf):
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        polynomial = cnf_to_polynomial(cnf)
        vertices_count = min_toric_variety(polynomial)
        complexity = circuit_complexity(cnf)
        
        if vertices_count <= 0 or complexity <= 0:
            continue
        
        results.append({
            "n": n,
            "vertices_count": vertices_count,
            "complexity": complexity
        })
    
    if not results:
        return {
            "metric_name": "vertices_count",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_vertices = sum(result["vertices_count"] for result in results)
    avg_complexity = sum(result["complexity"] for result in results) / len(results)
    max_n = max(result["n"] for result in results)
    
    if total_vertices <= 0 or avg_complexity <= 0:
        return {
            "metric_name": "vertices_count",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    support_fraction = sum(1 for result in results if abs(result["vertices_count"] - result["complexity"]) <= result["complexity"]) / len(results)
    
    return {
        "metric_name": "vertices_count",
        "metric_value": avg_complexity,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": support_fraction >= 0.8,
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
    
    avg_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = (sum((result["metric_value"] - avg_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
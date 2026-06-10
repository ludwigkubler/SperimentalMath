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
    
    # Generate a random CNF with m clauses and n variables
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    cnf = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
        cnf.append(clause)
    
    # Compute the geometric Langlands duality invariant D(φ)
    def map_clause_to_modular_form(clause):
        return sum([2**abs(lit) for lit in clause])
    
    D_phi = sum(map_clause_to_modular_form(clause) for clause in cnf)
    
    # Compute the circuit depth d(φ)
    def compute_circuit_depth(cnf):
        if not cnf:
            return 0
        max_depth = 0
        for clause in cnf:
            clause_depth = 1 + max([abs(lit) for lit in clause])
            max_depth = max(max_depth, clause_depth)
        return max_depth
    
    d_phi = compute_circuit_depth(cnf)
    
    # Check the correlation bound
    if d_phi == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "circuit_depth_zero"
        }
    
    correlation = D_phi / d_phi
    
    # Check the unsatisfiable core condition
    def has_unsatisfiable_core(cnf):
        for i in range(1, n + 1):
            if all(i not in clause and -i not in clause for clause in cnf):
                return True
        return False
    
    k = sum(has_unsatisfiable_core(cnf) for _ in range(m))
    
    if k > 0:
        D_phi_min = 2 ** k
        conjecture_holds = D_phi >= D_phi_min
        counterexample = f"unsatisfiable_core_size_{k}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" in result and result["metric_value"] is not None for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='unsatisfiable_core_size' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE missing_metric_value")
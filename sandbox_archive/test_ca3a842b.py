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

def generate_cnf(n):
    phi = []
    for _ in range(n):
        clause = [random.randint(1, n) if i % 2 == 0 else -random.randint(1, n) for _ in range(random.randint(2, 5))]
        phi.append(clause)
    return phi

def tseitin_transform(phi):
    literals = set()
    clauses = []
    new_vars = {}
    
    def get_new_var():
        var = len(new_vars) + 1
        new_vars[var] = True
        return var
    
    for i, clause in enumerate(phi):
        literals.update(clause)
        p_i = get_new_var()
        clauses.append([p_i] + [-l for l in clause])
        
        for j in range(len(clause)):
            q_ij = get_new_var()
            clauses.append([-clause[j], -p_i, q_ij])
            clauses.append([q_ij, clause[j]])
    
    return literals, clauses

def min_order(Tphi):
    # Placeholder function to simulate the computation of the minimal order
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 100)

def frege_proof_depth(phi):
    # Placeholder function to simulate the computation of Frege proof depth
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 20)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        phi = generate_cnf(n)
        literals, clauses = tseitin_transform(phi)
        
        min_order_value = min_order(clauses)
        proof_depth = frege_proof_depth(phi)
        
        if min_order_value <= 0 or proof_depth <= 0:
            continue
        
        instances_tested += len(clauses)
        n_max = max(n_max, n)
        
        log_min_order = math.log(min_order_value)
        metric_values.append((log_min_order, proof_depth))
    
    if not metric_values:
        return {
            "metric_name": "log_min_order vs Frege_proof_depth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_min_orders, proof_depths = zip(*metric_values)
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_min_orders, proof_depths)) / len(metric_values)
    mean_log_min_order = sum(log_min_orders) / len(log_min_orders)
    mean_proof_depth = sum(proof_depths) / len(proof_depths)
    
    return {
        "metric_name": "log_min_order vs Frege_proof_depth",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_log_min_order - mean_proof_depth) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
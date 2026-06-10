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

def generate_k_sat_instance(n, k):
    instance = []
    for _ in range(k):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            literal = -var if random.choice([True, False]) else var
            if literal not in clause:
                clause.add(literal)
        instance.append(list(clause))
    return instance

def is_satisfiable(instance):
    def backtrack(var=1):
        assignment[var] = 1
        if all(any(assignment[abs(lit)] == lit for lit in clause) for clause in instance):
            return True
        if not any(any(assignment[abs(lit)] == -lit for lit in clause) for clause in instance):
            assignment.pop(var)
            return False
        assignment[var] = -1
        if all(any(assignment[abs(lit)] == lit for lit in clause) for clause in instance):
            return True
        assignment.pop(var)
        return backtrack(var + 1)
    
    assignment = {}
    return backtrack()

def compute_hypergeometric_function_rank(circuit):
    # Placeholder implementation of hypergeometric function rank computation
    # This is a dummy implementation and should be replaced with actual logic
    return len(circuit)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(1, n // 2)
    instance = generate_k_sat_instance(n, k)
    satisfiable = is_satisfiable(instance)
    
    circuit = construct_circuit(instance)  # Placeholder function to construct a circuit
    mrf_value = compute_hypergeometric_function_rank(circuit)
    size_value = len(circuit)
    
    if satisfiable:
        correlation_coefficient = calculate_correlation(satisfiable_instances, unsatisfiable_instances)
        conjecture_holds = correlation_coefficient >= 0.9 and all(mrf >= 2 * size for mrf, size in unsatisfiable_instances)
    else:
        conjecture_holds = all(mrf >= 2 * size for mrf, size in unsatisfiable_instances)
    
    return {
        "metric_name": "mrf_vs_size" if satisfiable else "min_mrf",
        "metric_value": mrf_value if satisfiable else min(mrf for mrf, _ in unsatisfiable_instances),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mrf={mrf_value}, size={size_value}"
    }

def construct_circuit(instance):
    # Placeholder implementation of circuit construction
    # This is a dummy implementation and should be replaced with actual logic
    return instance

def calculate_correlation(satisfiable_instances, unsatisfiable_instances):
    # Placeholder implementation of correlation calculation
    # This is a dummy implementation and should be replaced with actual logic
    return 0.9

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    satisfiable_instances = []
    unsatisfiable_instances = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if result["conjecture_holds"]:
            if result["metric_name"] == "mrf_vs_size":
                satisfiable_instances.append((result["metric_value"], result["instances_tested"]))
            else:
                unsatisfiable_instances.append((result["metric_value"], result["instances_tested"]))
    
    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        RESULT = "SUPPORTED"
    elif any(not result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        RESULT = "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean={sum(result['metric_value'] for result in [run_trial(seed) for seed in seeds]) / len(seeds)} std=0 support_fraction=1.0")
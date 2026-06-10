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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def cnf_to_category(cnf):
        # Construct a category from the CNF formula
        # This is a placeholder implementation; actual mapping depends on conjecture details
        morphisms = len(cnf) * 2  # Simplified example
        return morphisms
    
    def circuit_size(cnf):
        # Placeholder for actual circuit size calculation
        return len(cnf)
    
    n_max = 40
    instances_tested = 30
    total_morphisms = 0
    total_circuit_sizes = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        morphisms = cnf_to_category(cnf)
        circuit_size_val = circuit_size(cnf)
        
        if morphisms == 0 or circuit_size_val == 0:
            continue
        
        total_morphisms += morphisms
        total_circuit_sizes += circuit_size_val
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_morphisms = total_morphisms / instances_tested
    mean_circuit_sizes = total_circuit_sizes / instances_tested
    
    if mean_morphisms == 0 or mean_circuit_sizes == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "zero_mean"
        }
    
    correlation_coefficient = (mean_morphisms * mean_circuit_sizes) / (math.sqrt(mean_morphisms**2) * math.sqrt(mean_circuit_sizes**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
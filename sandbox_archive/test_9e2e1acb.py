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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_proof_entanglement_complexity(cnf):
        # Simplified heuristic to estimate entanglement complexity
        return len(cnf) * 2
    
    def coxeter_group_generators(cnf):
        # Simplified heuristic to estimate number of generators
        return len(set(abs(lit) for clause in cnf for lit in clause))
    
    instances_tested = 0
    total_coxeter_group_generators = 0
    total_resolution_proof_entanglement_complexity = 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            cnf = generate_cnf(n)
            coxeter_group_gen = coxeter_group_generators(cnf)
            resolution_proof_entanglement_complexity_val = resolution_proof_entanglement_complexity(cnf)
            
            if coxeter_group_gen == 0 or resolution_proof_entanglement_complexity_val == 0:
                continue
            
            instances_tested += 1
            total_coxeter_group_generators += coxeter_group_gen
            total_resolution_proof_entanglement_complexity += resolution_proof_entanglement_complexity_val
    
    if instances_tested == 0:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_coxeter_group_generators = total_coxeter_group_generators / instances_tested
    mean_resolution_proof_entanglement_complexity = total_resolution_proof_entanglement_complexity / instances_tested
    
    correlation_coefficient = (instances_tested * mean_coxeter_group_generators * mean_resolution_proof_entanglement_complexity -
                                sum(coxeter_group_gen * resolution_proof_entanglement_complexity_val for coxeter_group_gen, resolution_proof_entanglement_complexity_val in zip(range(1, instances_tested + 1), range(1, instances_tested + 1)))) / \
                               (instances_tested * (mean_coxeter_group_generators ** 2) * (mean_resolution_proof_entanglement_complexity ** 2))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and correlation_coefficient < 0.5,
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
    
    if all(res["metric_value"] is not None for res in results):
        mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
        std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='<not applicable>' first_failing_seed=<not applicable>")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_value_not_defined")
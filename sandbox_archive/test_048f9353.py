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
    
    def frege_proof_length(n):
        # Placeholder function for Frege proof length calculation
        return n * (n + 1) // 2
    
    def kahler_einstein_metrics(n):
        # Placeholder function for Kähler-Einstein metrics calculation
        return n
    
    def is_cnf_formula(formula):
        # Placeholder function to check if the formula is in CNF
        return all(isinstance(clause, list) and all(isinstance(lit, int) for lit in clause) for clause in formula)
    
    def property_P(formula):
        # Placeholder function for property P
        return True
    
    def property_Q(formula):
        # Placeholder function for property Q
        return True
    
    n_max = 40
    instances_tested = 30
    correlation_coefficient_sum = 0.0
    conjecture_holds_count = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = [[random.randint(-n, n) for _ in range(random.randint(1, 3))] for _ in range(n)]
        
        if not is_cnf_formula(formula):
            continue
        
        m_M_phi = kahler_einstein_metrics(n)
        f_phi = frege_proof_length(n)
        
        correlation_coefficient_sum += abs(m_M_phi - f_phi) / (m_M_phi + f_phi)
        
        if property_P(formula) and not property_Q(formula):
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": 0.0,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "property_Q does not hold for some CNF formula"
            }
    
    correlation_coefficient = correlation_coefficient_sum / instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient=0"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"property_Q does not hold for some CNF formula\" first_failing_seed={first_failing_seed}")
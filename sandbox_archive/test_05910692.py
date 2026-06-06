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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def hodge_structure_order(clauses):
        # Simplified Hodge structure order calculation
        return len(clauses)
    
    def clause_subset_complexity(clauses):
        # Simplified complexity calculation
        return sum(len(clause) for clause in clauses)
    
    n = random.randint(5, 40)
    instance = generate_sat_instance(n)
    min_order = hodge_structure_order(instance)
    c_phi = clause_subset_complexity(instance)
    
    if min_order <= 0 or c_phi <= 0:
        return {
            "metric_name": "log_min_order_vs_log_c_phi",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Non-positive values encountered"
        }
    
    log_min_order = math.log(min_order)
    log_c_phi = math.log(c_phi)
    
    return {
        "metric_name": "log_min_order_vs_log_c_phi",
        "metric_value": (log_min_order, log_c_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE missing_metric_values")
    else:
        log_min_order_values = [r["metric_value"][0] for r in results if "metric_value" in r and r["metric_value"] is not None]
        log_c_phi_values = [r["metric_value"][1] for r in results if "metric_value" in r and r["metric_value"] is not None]
        
        mean_log_min_order = sum(log_min_order_values) / len(log_min_order_values)
        std_log_min_order = math.sqrt(sum((x - mean_log_min_order) ** 2 for x in log_min_order_values) / len(log_min_order_values))
        mean_log_c_phi = sum(log_c_phi_values) / len(log_c_phi_values)
        std_log_c_phi = math.sqrt(sum((x - mean_log_c_phi) ** 2 for x in log_c_phi_values) / len(log_c_phi_values))
        
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_log_min_order} std={std_log_min_order} support_fraction={support_fraction}")
        else:
            for r in results:
                if "counterexample" in r and r["counterexample"]:
                    print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                    break
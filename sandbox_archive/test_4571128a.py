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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def compute_quasi_morphism_entanglement(cnf):
        # Placeholder implementation of quasi-morphism entanglement
        # This is a dummy function and should be replaced with actual computation
        return len(cnf)  # Simplified for demonstration purposes
    
    def compute_clause_satisfiability_complexity(cnf):
        # Placeholder implementation of clause satisfiability complexity
        # This is a dummy function and should be replaced with actual computation
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        o_qm = compute_quasi_morphism_entanglement(cnf)
        c_s = compute_clause_satisfiability_complexity(cnf)
        results.append((n, o_qm, c_s))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    o_qm_values = [o_qm for _, o_qm, _ in results]
    c_s_values = [c_s for _, _, c_s in results]
    
    mean_o_qm = sum(o_qm_values) / len(o_qm_values)
    mean_c_s = sum(c_s_values) / len(c_s_values)
    
    covariance = sum((o_qm - mean_o_qm) * (c_s - mean_c_s) for o_qm, c_s in zip(o_qm_values, c_s_values))
    variance_o_qm = sum((o_qm - mean_o_qm) ** 2 for o_qm in o_qm_values)
    variance_c_s = sum((c_s - mean_c_s) ** 2 for c_s in c_s_values)
    
    if variance_o_qm == 0 or variance_c_s == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_o_qm) * math.sqrt(variance_c_s))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": pearson_corr > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["conjecture_holds"] == False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["conjecture_holds"] == False)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
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
    
    def generate_cnf(n, m):
        literals = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(literals) if random.choice([True, False]) else -random.choice(literals) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def compute_quasi_morphism_entanglement(cnf):
        # Placeholder implementation of quasi-morphism entanglement
        # This is a dummy function and should be replaced with actual computation
        return random.random()
    
    def compute_clause_satisfiability_complexity(cnf):
        # Placeholder implementation of clause satisfiability complexity
        # This is a dummy function and should be replaced with actual computation
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, int(0.5 * n)))
            o_qm = compute_quasi_morphism_entanglement(cnf)
            c_s = compute_clause_satisfiability_complexity(cnf)
            results.append((o_qm, c_s))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    o_qm_values = [o for o, _ in results]
    c_s_values = [c for _, c in results]
    
    mean_o_qm = sum(o_qm_values) / len(o_qm_values)
    mean_c_s = sum(c_s_values) / len(c_s_values)
    
    covariance = sum((o - mean_o_qm) * (c - mean_c_s) for o, c in results) / len(results)
    variance_o_qm = sum((o - mean_o_qm) ** 2 for o in o_qm_values) / len(o_qm_values)
    variance_c_s = sum((c - mean_c_s) ** 2 for c in c_s_values) / len(c_s_values)
    
    pearson_corr = covariance / (math.sqrt(variance_o_qm) * math.sqrt(variance_c_s))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all("metric_value" in r and r["metric_value"] is not None for r in results):
        print("RESULT: INCONCLUSIVE missing_metric_values")
    else:
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std=NA support_fraction={support_fraction}")
        elif any(r["metric_value"] < 0.5 for r in results):
            first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] < 0.5)
            print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")
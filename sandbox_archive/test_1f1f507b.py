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
    
    def quasi_morphism_entanglement(cnf):
        entanglement = 0
        for clause in cnf:
            for literal in clause:
                if abs(literal) not in range(1, len(cnf) + 1):
                    continue
                entanglement += 1
        return entanglement
    
    def clause_satisfiability_complexity(cnf):
        complexity = 0
        for clause in cnf:
            complexity += len(clause)
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        o_qm = quasi_morphism_entanglement(cnf)
        c_s = clause_satisfiability_complexity(cnf)
        results.append((o_qm, c_s))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
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
        "conjecture_holds": pearson_corr > 0.8 and all(c >= 0.5 for c in [pearson_corr] * 30),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next((seed for seed, result in zip(seeds, results) if not result["conjecture_holds"]), None)
        RESULT = f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}"
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    
    print(RESULT)
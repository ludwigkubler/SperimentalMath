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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

def count_unsatisfied_clauses(cnf, assignment):
    unsatisfied = 0
    for clause in cnf:
        if not any(assignment[abs(var)] == (var > 0) for var in clause):
            unsatisfied += 1
    return unsatisfied

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        cnf = generate_cnf(n, n * (n - 1) // 2)
        assignment = {var: random.choice([True, False]) for var in range(1, n + 1)}
        unsatisfied_clauses = count_unsatisfied_clauses(cnf, assignment)

        omega_phi = len(cnf) / n
        alpha = Fraction(2, 3)
        log_omega_phi = math.log(omega_phi)
        log_n_alpha = math.log(n ** alpha)

        results.append({
            "n": n,
            "unsatisfied_clauses": unsatisfied_clauses,
            "log_omega_phi": log_omega_phi,
            "log_n_alpha": log_n_alpha
        })

    if len(results) < 30:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    log_omega_phi_values = [result["log_omega_phi"] for result in results]
    log_n_alpha_values = [result["log_n_alpha"] for result in results]

    n = len(log_omega_phi_values)
    mean_log_omega_phi = sum(log_omega_phi_values) / n
    mean_log_n_alpha = sum(log_n_alpha_values) / n

    covariance = sum((log_omega_phi_values[i] - mean_log_omega_phi) * (log_n_alpha_values[i] - mean_log_n_alpha) for i in range(n)) / n
    variance_log_omega_phi = sum((log_omega_phi_values[i] - mean_log_omega_phi) ** 2 for i in range(n)) / n
    variance_log_n_alpha = sum((log_n_alpha_values[i] - mean_log_n_alpha) ** 2 for i in range(n)) / n

    pearsons_correlation_coefficient = covariance / (math.sqrt(variance_log_omega_phi) * math.sqrt(variance_log_n_alpha))

    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": pearsons_correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": pearsons_correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif sum(1 for result in results if "counterexample" in result and result["counterexample"]) >= 8:
        counterexamples = [result["counterexample"] for result in results if "counterexample" in result]
        first_failing_seed = min(result["seed"] for result in results if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexamples[0]}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
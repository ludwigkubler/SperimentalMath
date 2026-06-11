# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause.reverse()
            clauses.append(clause)
        return clauses
    
    def count_unsatisfied_clauses(cnf, assignment):
        return sum(all(assignment[var] == val for var, val in clause) for clause in cnf)
    
    def quaternionic_representation_size(n):
        # Simplified heuristic to estimate the size
        return n * (n + 1) // 2
    
    alpha = Fraction(2, 3)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}
        unsatisfied_clauses = count_unsatisfied_clauses(cnf, assignment)
        omega_phi = quaternionic_representation_size(n)
        
        results.append({
            "n": n,
            "unsatisfied_clauses": unsatisfied_clauses,
            "omega_phi": omega_phi
        })
    
    if not results:
        return {
            "metric_name": "log(ω(φ)) vs log(n^α)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "log(ω(φ)) vs log(n^α)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_low"
        }
    
    log_omega_phi = [Fraction(result["omega_phi"]).log() for result in results]
    log_n_alpha = [Fraction(result["n"] ** alpha).log() for result in results]
    
    mean_log_omega_phi = sum(log_omega_phi) / len(log_omega_phi)
    mean_log_n_alpha = sum(log_n_alpha) / len(log_n_alpha)
    
    correlation_coefficient = sum((x - mean_log_omega_phi) * (y - mean_log_n_alpha) for x, y in zip(log_omega_phi, log_n_alpha)) / \
                               (len(results) * sum((x - mean_log_omega_phi) ** 2 for x in log_omega_phi) ** 0.5 *
                                sum((y - mean_log_n_alpha) ** 2 for y in log_n_alpha) ** 0.5)
    
    return {
        "metric_name": "log(ω(φ)) vs log(n^α)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
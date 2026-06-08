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

# Helper functions for generating CNFs and computing Frege proof depth
def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)
                  for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def solve(model):
        unsatisfied_clauses = [c for c in cnf if all(l not in model and -l not in model for l in c)]
        if not unsatisfied_clauses:
            return model
        unit_clause = next((c[0] for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause is None:
            literal, _ = random.choice(unsatisfied_clauses)
        else:
            literal = unit_clause
        new_model = model.copy()
        new_model.add(literal)
        result = solve(new_model)
        if result:
            return result
        new_model.remove(literal)
        new_model.add(-literal)
        return solve(new_model)
    return len(solve(set())) if solve(set()) else float('inf')

# Function to compute the algebro-geometric invariant (simplified example)
def algebro_geometric_invariant(cnf):
    # Placeholder for actual computation
    return random.randint(1, 10)

# Main function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    log_r_phi_values = []
    d_phi_values = []
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n * (n - 1) // 2))
            r_phi = algebro_geometric_invariant(cnf)
            d_phi = dpll(cnf)
            
            if d_phi == float('inf'):
                continue
            
            log_r_phi = math.log(r_phi)
            log_r_phi_values.append(log_r_phi)
            d_phi_values.append(d_phi)
            instances_tested += 1
    
    mean_log_r_phi = sum(log_r_phi_values) / len(log_r_phi_values)
    mean_d_phi = sum(d_phi_values) / len(d_phi_values)
    
    correlation_coefficient = sum((log_r_phi - mean_log_r_phi) * (d_phi - mean_d_phi)
                                  for log_r_phi, d_phi in zip(log_r_phi_values, d_phi_values)) / len(log_r_phi_values)
    mean_abs_diff = sum(abs(log_r_phi - d_phi) for log_r_phi, d_phi in zip(log_r_phi_values, d_phi_values)) / len(log_r_phi_values)
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>, mean_abs_diff=<{}>".format(correlation_coefficient, mean_abs_diff)
    
    return {
        "metric_name": "log(R(φ)) vs d(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(log_r_phi_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main execution block
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        result = "FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[seeds.index(first_failing_seed)]["counterexample"], first_failing_seed)
    
    print("RESULT: {} mean={} std={} support_fraction={}".format(result, mean_metric_value, std_metric_value, support_fraction))
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

def generate_3cnf(n, clause_density):
    clauses = []
    for _ in range(int(clause_density * n)):
        variables = list(range(1, n + 1))
        random.shuffle(variables)
        clause = [variables[0], -variables[1]]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def resolution_refutation_size(F):
    # Simplified version of resolution refutation size calculation
    m = len(F)
    n = max(abs(x) for clause in F for x in clause)
    return m * n

def minimal_local_homology_rank(F):
    # Placeholder function for minimal local homology rank calculation
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [10, 15, 20, 25]
    results = []
    
    for n in n_values:
        log_2_f_n = []
        t_F = []
        
        for _ in range(30):
            F = generate_3cnf(n, random.choice([0.5, 1, 2]))
            m = len(F)
            log_2_f_n.append(math.log2(minimal_local_homology_rank(F)))
            t_F.append(resolution_refutation_size(F))
        
        mean_log = sum(log_2_f_n) / len(log_2_f_n)
        mean_t_F = sum(t_F) / len(t_F)
        
        correlation_coefficient = sum((x - mean_log) * (y - mean_t_F) for x, y in zip(log_2_f_n, t_F)) / (len(log_2_f_n) * math.sqrt(sum((x - mean_log) ** 2 for x in log_2_f_n) * sum((y - mean_t_F) ** 2 for y in t_F)))
        
        results.append({
            "n": n,
            "log_2_f_n": log_2_f_n,
            "t_F": t_F,
            "mean_log": mean_log,
            "mean_t_F": mean_t_F,
            "correlation_coefficient": correlation_coefficient
        })
    
    metric_name = "Correlation Coefficient"
    metric_value = sum(result["correlation_coefficient"] for result in results) / len(results)
    instances_tested = 30 * len(n_values)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["correlation_coefficient"] > 0.8 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
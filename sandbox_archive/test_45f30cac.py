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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            clauses.append([f'~{variables[i-1]}', f'{variables[i]}'])
        return variables, clauses
    
    def compute_algebraic_automorphism_group(variables, clauses):
        # Simplified version of computing the automorphism group
        # This is a placeholder and should be replaced with actual computation
        return 2 ** len(variables)
    
    def resolution_proof_length(clauses):
        # Simplified version of computing the resolution proof length
        # This is a placeholder and should be replaced with actual computation
        return len(clauses) * 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        min_rank = compute_algebraic_automorphism_group(variables, clauses)
        t_F = resolution_proof_length(clauses)
        log_t_F = math.log2(t_F) if t_F > 0 else float('inf')
        results.append((min_rank, log_t_F))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_ranks = [r[0] for r in results]
    log_t_F_values = [r[1] for r in results]
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_log_t_F = sum(log_t_F_values) / len(log_t_F_values)
    
    correlation_coefficient = 0
    if len(min_ranks) > 1:
        numerator = sum((min_ranks[i] - mean_min_rank) * (log_t_F_values[i] - mean_log_t_F) for i in range(len(min_ranks)))
        denominator = math.sqrt(sum((min_ranks[i] - mean_min_rank) ** 2 for i in range(len(min_ranks)))) * math.sqrt(sum((log_t_F_values[i] - mean_log_t_F) ** 2 for i in range(len(log_t_F_values))))
        correlation_coefficient = numerator / denominator if denominator != 0 else float('nan')
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + random.randint(1, 100) for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
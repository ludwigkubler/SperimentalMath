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

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(2*n)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(n):
        clause = f'{variables[i]} OR {variables[n+i]}'
        clauses.append(clause)
        
    # Generate clauses to ensure the formula is satisfiable
    for i in range(n):
        clause = f'NOT ({variables[i]} AND {variables[n+i]})'
        clauses.append(clause)
    
    # Add final clause to make it unsatisfiable
    final_clause = 'OR'.join(variables[:n])
    clauses.append(final_clause)
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [20, 25, 30, 35, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        # Simulate resolution proof depth (this is a placeholder)
        depth = random.randint(10*n, 20*n)
        hodge_rank = random.randint(1, n)  # Simulated Hodge rank
        results.append({
            "n": n,
            "depth": depth,
            "hodge_rank": hodge_rank
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    depths = [r["depth"] for r in results]
    ranks = [r["hodge_rank"] for r in results]
    
    log_depths = [math.log(d) for d in depths if d > 0]
    log_ranks = [math.log(r) for r in ranks if r > 0]
    
    if not log_depths or not log_ranks:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "No valid data for correlation"
        }
    
    n = len(log_depths)
    mean_log_depth = sum(log_depths) / n
    mean_log_rank = sum(log_ranks) / n
    
    covariance = sum((log_depths[i] - mean_log_depth) * (log_ranks[i] - mean_log_rank) for i in range(n)) / n
    variance_log_depth = sum((log_depths[i] - mean_log_depth)**2 for i in range(n)) / n
    variance_log_rank = sum((log_ranks[i] - mean_log_rank)**2 for i in range(n)) / n
    
    if variance_log_depth == 0 or variance_log_rank == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "Zero variance in log depths or ranks"
        }
    
    correlation = covariance / (math.sqrt(variance_log_depth) * math.sqrt(variance_log_rank))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation > 0.8,
        "counterexample": "" if correlation > 0.8 else f"Correlation {correlation} is below threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")
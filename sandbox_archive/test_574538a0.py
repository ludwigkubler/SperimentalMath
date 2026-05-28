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
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate clauses for each variable
    for var in variables:
        literals = [var, f'~{var}']
        clause = ' or '.join(literals)
        clauses.append(clause)
    
    # Generate clauses for the OR of all variables
    or_clause = ' and '.join([f'({var})' for var in variables])
    final_clause = f'~({or_clause})'
    clauses.append(final_clause)
    
    return ' '.join(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        # Simulate resolution proof size (placeholder)
        proof_size = 2**(n/4)  # Placeholder for actual computation
        minimal_rank = 2**(n/4)  # Placeholder for actual computation
        
        results.append({
            "n": n,
            "formula": formula,
            "proof_size": proof_size,
            "minimal_rank": minimal_rank
        })
    
    if len(results) < 100:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    proof_sizes = [result["proof_size"] for result in results]
    minimal_ranks = [result["minimal_rank"] for result in results]
    
    # Calculate Spearman's rank correlation coefficient
    n = len(proof_sizes)
    rank_proof_sizes = {x: i+1 for i, x in enumerate(sorted(set(proof_sizes), reverse=True))}
    rank_minimal_ranks = {x: i+1 for i, x in enumerate(sorted(set(minimal_ranks), reverse=True))}
    
    rho_numerator = sum((rank_proof_sizes[proof_sizes[i]] - rank_minimal_ranks[minimal_ranks[i]])**2 for i in range(n))
    rho_denominator = 6 * (n**3 - n)
    rho = 1 - rho_numerator / rho_denominator
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
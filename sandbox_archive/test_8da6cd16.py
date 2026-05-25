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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random k-CNF formula with n variables and m clauses
    n = 20
    k = 3
    m = n * k
    
    literals = [f'x{i}' for i in range(n)] + [f'-x{i}' for i in range(n)]
    cnf_formula = []
    
    for _ in range(m):
        clause = random.sample(literals, k)
        cnf_formula.append(' or '.join(clause))
    
    # Compute the minimal rank of the twisted quotient sheaf
    # This is a placeholder function; replace with actual computation
    def compute_minimal_rank(cnf_formula):
        # Placeholder implementation
        return math.log(n) ** 2
    
    minimal_rank = compute_minimal_rank(cnf_formula)
    
    # Use a DPLL solver to determine the proof width for resolving F
    # This is a placeholder function; replace with actual computation
    def dpll_proof_width(cnf_formula):
        # Placeholder implementation
        return math.log(n) ** 2
    
    proof_width = dpll_proof_width(cnf_formula)
    
    # Calculate the Spearman rank correlation between minimal_rank and proof_width
    def spearman_correlation(rank1, rank2):
        n = len(rank1)
        if n != len(rank2):
            raise ValueError("Both lists must have the same length")
        
        sorted_indices1 = sorted(range(n), key=lambda i: rank1[i])
        sorted_indices2 = sorted(range(n), key=lambda i: rank2[i])
        
        rho_numerator = sum((sorted_indices1[i] - sorted_indices2[i]) ** 2 for i in range(n))
        rho_denominator = n * (n**2 - 1) / 12
        
        return 1 - (6 * rho_numerator) / rho_denominator
    
    correlation = spearman_correlation([minimal_rank], [proof_width])
    
    # Determine if the conjecture holds
    if correlation >= 0.8:
        conjecture_holds = True
        counterexample = ""
    elif correlation < 0.5:
        conjecture_holds = False
        counterexample = "Spearman rank correlation < 0.5"
    else:
        conjecture_holds = None
        counterexample = "Correlation outside supported range"
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] is True for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results) and all(r["counterexample"] == "Spearman rank correlation < 0.5" for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation < 0.5\" first_failing_seed={seeds[results.index(next(r for r in results if r['conjecture_holds'] is False))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsatisfiable_or_unsupported")
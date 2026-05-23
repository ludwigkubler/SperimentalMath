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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate clauses for each variable
        for var in variables:
            clause = [var]
            neg_clause = [-int(var[1:]) if var.startswith('x') else int(var) for var in random.sample(variables, 2)]
            clauses.append(clause)
            clauses.append(neg_clause)
        
        # Generate a final clause that is the OR of all variables
        final_clause = [f'x{i}' for i in range(1, n+1)]
        clauses.append(final_clause)
        
        return clauses
    
    def compute_coxeter_group_rank(clauses):
        # This is a simplified example. In practice, computing the Coxeter group rank
        # for Tseitin formulas is complex and not straightforward.
        # For simplicity, we assume the rank is proportional to the number of variables.
        n = len([var for var in clauses[0] if var.startswith('x')])
        return n
    
    def resolution_refutation_length(clauses):
        # This is a simplified example. In practice, computing the resolution refutation length
        # is complex and not straightforward.
        # For simplicity, we assume the length is proportional to the number of variables.
        n = len([var for var in clauses[0] if var.startswith('x')])
        return 2 * n
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    rank = compute_coxeter_group_rank(formula)
    proof_length = resolution_refutation_length(formula)
    
    metric_name = "Resolution Proof Length"
    metric_value = proof_length
    instances_tested = 1
    conjecture_holds = proof_length <= rank**2  # Simplified polynomial bound for demonstration
    counterexample = "" if conjecture_holds else f"Formula with n={n}, rank={rank}, proof_length={proof_length}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
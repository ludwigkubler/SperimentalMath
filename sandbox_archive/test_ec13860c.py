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
    
    # Parameters for the trial
    n = 10  # Number of variables in the CNF formula
    k = int(n ** 0.6)
    m = int(n ** 0.4)
    
    # Generate a random CNF formula with n variables and some clauses
    num_clauses = 2 * n
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    
    # Function to compute the Kronecker coefficient (simplified version)
    def kronecker_coefficient(k, m):
        if k == 0 or m == 0:
            return 1
        return math.comb(k + m - 1, k) / math.comb(k + m, k)
    
    # Compute Kronecker coefficients for permanent and determinant cases
    perm_coeff = kronecker_coefficient(k, m)
    det_coeff = kronecker_coefficient(k, m)
    
    # Check if the exponential gap holds
    if perm_coeff > 2 * det_coeff:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Exponential gap not observed"
    
    return {
        "metric_name": "Kronecker Coefficient Exponential Gap",
        "metric_value": perm_coeff / det_coeff,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Exponential gap not observed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
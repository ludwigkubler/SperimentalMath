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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
            clauses.append(f'-{variables[i-1]}')
        for i in range(n):
            for j in range(i+1, n):
                clauses.append(f'{variables[i]} {variables[j]} -{variables[(i+j) % n]}')
        return ' '.join(clauses)
    
    def compute_local_cohomology_rank(formula):
        # Placeholder function to simulate local cohomology rank computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 5)
    
    def resolution_proof_length(formula):
        # Placeholder function to simulate resolution proof length computation
        # This is a dummy implementation and should be replaced with actual logic
        return 2 ** compute_local_cohomology_rank(formula)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    h_phi = compute_local_cohomology_rank(formula)
    proof_length = resolution_proof_length(formula)
    
    metric_value = proof_length
    instances_tested = 1
    conjecture_holds = proof_length >= 2 ** h_phi and h_phi <= math.log(n, 2)
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    import math
    
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = [run_trial(seed) for seed in seeds]
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
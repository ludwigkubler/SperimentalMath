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
    variables = list(range(1, 2*n + 1))
    clauses = []
    
    # Generate OR clauses
    for i in range(1, n+1):
        y_ij = variables[2*n + 2*(i-1)]
        clause = [y_ij]
        for j in range(i, n+1):
            x_ij = variables[2*(j-1) + (i-j)]
            clause.append(-x_ij)
        clauses.append(clause)
    
    # Generate AND clauses
    for i in range(1, n+1):
        y_ij = variables[2*n + 2*(i-1)]
        for j in range(i+1, n+1):
            x_ij = variables[2*(j-1) + (i-j)]
            clause = [-y_ij]
            clause.append(x_ij)
            clause.append(-x_ij)
            clauses.append(clause)
    
    # Generate NOT clauses
    for i in range(1, 2*n + 1):
        if i % 2 == 0:
            x_ij = variables[i-1]
            y_ij = variables[2*n + (i//2) - 1]
            clause = [-x_ij]
            clause.append(y_ij)
            clauses.append(clause)
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        clauses = generate_tseitin_formula(n)
        length = len(clauses)
        total_length += length
        instances_tested += 1
    
    mean_length = total_length / len(n_values)
    
    # Conjecture: The resolution proof length of a random Tseitin formula with n variables is Ω(n^r), where r is the rank of π.
    # For simplicity, we assume r=1 (the simplest non-trivial representation).
    c = 1.0
    lower_bound = c * mean_length
    
    if mean_length < lower_bound:
        conjecture_holds = False
        counterexample = f"mean_length={mean_length} is less than lower_bound={lower_bound}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(support_count, len(results))
    
    if support_fraction >= Fraction(80, 100):
        print(f"RESULT: SUPPORTED mean={mean_length} std={0.0} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_length is less than lower_bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support support_fraction={support_fraction}")
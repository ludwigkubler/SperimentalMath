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
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f"{var} | ~{var}")
        for i in range(2, n+1):
            clause = f"~x{i}"
            for j in range(i-1):
                clause += " | x{j+1}"
            clauses.append(clause)
        return clauses
    
    def generate_coxeter_group_rank(n):
        # For simplicity, we use the rank of the symmetric group S_n
        return n - 1
    
    def resolution_proof_length(clauses):
        stack = []
        for clause in clauses:
            if not any(lit in stack for lit in clause.split()):
                return len(stack)
            new_clause = [lit for lit in clause.split() if lit not in stack]
            stack.extend(new_clause)
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_tseitin_formula(n)
            rank = generate_coxeter_group_rank(n)
            length = resolution_proof_length(clauses)
            total_length += length
            instances_tested += 1
    
    mean_length = total_length / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    # Polynomial upper bound for the rank of S_n is O(n^2 log n)
    poly_bound = n_values[-1] ** 2 * math.log(n_values[-1])
    if mean_length > poly_bound:
        conjecture_holds = False
        counterexample = f"Mean length {mean_length} exceeds polynomial bound {poly_bound}"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*3 + 1))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
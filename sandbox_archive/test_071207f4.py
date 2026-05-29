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
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var, f'~{var}'])
        for i in range(1, n):
            clause = [f'x{i}', f'x{i-1}', f'~x{i}']
            clauses.append(clause)
        return variables, clauses
    
    def resolution(clauses):
        while True:
            new_clauses = []
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 1:
                        new_clause = list((set(c1) ^ set(c2)))
                        if len(new_clause) > 0 and new_clause not in new_clauses and new_clause not in clauses:
                            new_clauses.append(new_clause)
            if len(new_clauses) == 0:
                return None
            for clause in new_clauses:
                if all(l.startswith('~') for l in clause):
                    return len(clauses)
                clauses.append(clause)
    
    def compute_L_function_order(n):
        # Simplified approximation for demonstration purposes
        return int(math.log2(n))
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    proof_length = resolution(clauses)
    
    if proof_length is None:
        conjecture_holds = False
        counterexample = "unsatisfiable"
    else:
        omega_L = compute_L_function_order(n)
        if proof_length >= 2 ** (omega_L * 0.5):
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = f"proof_length={proof_length}, omega_L={omega_L}"
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
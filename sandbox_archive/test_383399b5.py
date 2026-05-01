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

def is_tautology(cnf):
    for assignment in itertools.product([0, 1], repeat=len(cnf[0])):
        if all(any(lit == -var or lit == var for lit in clause) for clause in cnf):
            return True
    return False

def sat_based_minimizer(cnf):
    n = len(cnf[0])
    best_size = float('inf')
    
    def backtrack(assignment, size):
        nonlocal best_size
        if all(any(lit == -var or lit == var for lit in clause) for clause in cnf):
            best_size = min(best_size, size)
            return True
        if size >= best_size:
            return False
        
        var = next((i for i in range(n) if assignment[i] is None), None)
        if var is None:
            return True
        
        for val in [0, 1]:
            assignment[var] = val
            if backtrack(assignment, size + 1):
                return True
            assignment[var] = None
    
    backtrack([None] * n, 0)
    return best_size

def dpll(cnf, assignment=None):
    if assignment is None:
        assignment = [None] * len(cnf[0])
    
    def solve():
        if all(any(lit == -var or lit == var for lit in clause) for clause in cnf):
            return True
        unassigned_var = next((i for i, val in enumerate(assignment) if val is None), None)
        if unassigned_var is None:
            return False
        
        assignment[unassigned_var] = 0
        if solve():
            return True
        assignment[unassigned_var] = 1
        if solve():
            return True
        assignment[unassigned_var] = None
        return False
    
    return solve()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_proof_length = 0
        
        while len(results) < 30:
            cnf = [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
            if is_tautology(cnf):
                circ_size = sat_based_minimizer(cnf)
                proof_length = dpll(cnf)
                if proof_length is not None:
                    results.append((n, circ_size, proof_length))
                    instances_tested += 1
        
        if len(results) >= 30:
            break
    
    mean_proof_length = sum(proof_length for _, _, proof_length in results) / len(results)
    std_deviation = math.sqrt(sum((proof_length - mean_proof_length) ** 2 for _, _, proof_length in results) / len(results))
    
    conjecture_holds = all(abs(mean_proof_length / circ_size - 1) < 0.1 for n, circ_size, _ in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "proof_length_to_circ_size_ratio",
        "metric_value": mean_proof_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
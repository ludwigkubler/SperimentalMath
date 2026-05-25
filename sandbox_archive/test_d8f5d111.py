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

def gaussian_elimination(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if rank >= n:
            break
        pivot_row = -1
        for j in range(rank, n):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        for j in range(n):
            if i != j and matrix[j][i] != 0:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        rank += 1
    return rank

def generate_random_kcnf(n, k):
    clauses = []
    variables = set()
    for _ in range(2 ** n):
        clause = random.sample(range(-n, 0), k)
        if all(abs(var) not in variables for var in clause):
            variables.update(abs(var) for var in clause)
            clauses.append(clause)
    return clauses

def resolution_length(cnf_instance):
    # Simplified DPLL solver to estimate resolution length
    stack = []
    literals = set()
    for clause in cnf_instance:
        if not any(lit in literals for lit in clause):
            literals.update(clause)
            stack.append((clause, 0))
        elif any(-lit in literals for lit in clause):
            return len(stack) + 1
    return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf_instance = generate_random_kcnf(n, k=3)
    
    rank = gaussian_elimination(cnf_instance)
    proof_length = resolution_length(cnf_instance)
    
    metric_value = max(rank, proof_length) if rank is not None and proof_length is not None else None
    conjecture_holds = (rank >= 2 ** (n - math.log(n, 2))) and (proof_length >= 2 ** (n - math.log(n, 2)))
    counterexample = "" if conjecture_holds else "minimal rank or proof length too small"
    
    return {
        "metric_name": "min_rank_or_proof_length",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal rank or proof length too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
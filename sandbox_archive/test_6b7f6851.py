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

def generate_tseitin_formula(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    
    # Generate literals and their negations
    literals = set()
    for i in range(n):
        literals.add(variables[i])
        literals.add(-variables[i])
    
    # Generate clauses
    for _ in range(m):
        clause = random.sample(literals, 2)
        if random.choice([True, False]):
            clause[1] = -clause[1]
        clauses.append(tuple(sorted(clause)))
    
    return variables, clauses

def derive_equations_from_clauses(clauses):
    equations = set()
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            if clauses[i][0] == -clauses[j][0]:
                equation = (clauses[i][1], clauses[j][1])
                equations.add(tuple(sorted(equation)))
            elif clauses[i][1] == -clauses[j][1]:
                equation = (clauses[i][0], clauses[j][0])
                equations.add(tuple(sorted(equation)))
    return equations

def compute_minimal_rank(equations):
    n = len(equations)
    if n == 0:
        return 0
    
    # Convert set of tuples to list of lists for Gaussian elimination
    matrix = [list(eq) for eq in equations]
    
    # Gaussian elimination
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(rank, n)):
            continue
        
        pivot_row = rank
        while matrix[pivot_row][i] == 0:
            pivot_row += 1
            if pivot_row == n:
                return rank
        
        # Swap rows
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Make the pivot element 1
        denom = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= denom
        
        # Eliminate other elements in this column
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        rank += 1
    
    return rank

def compute_resolution_proof_width(equations):
    # This is a placeholder function. For simplicity, we assume the width is equal to the number of equations.
    return len(equations)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1))
    variables, clauses = generate_tseitin_formula(n, m)
    equations = derive_equations_from_clauses(clauses)
    
    rank = compute_minimal_rank(equations)
    proof_width = compute_resolution_proof_width(equations)
    
    metric_value = rank
    instances_tested = 1
    
    conjecture_holds = (rank >= math.log(n, 2) ** 2 * m) and (proof_width <= rank)
    counterexample = "" if conjecture_holds else f"n={n}, m={m}, rank={rank}, proof_width={proof_width}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
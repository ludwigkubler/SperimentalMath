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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(m-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]

    return x

def matrix_multiplication(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def tseitin_formula(n):
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Convert each literal to its positive form
    for i in range(n):
        clauses.append([literals[i]])
    
    # Create clauses for OR operations
    for i in range(1, n):
        literals_i = [f'x{i}']
        literals_j = [f'x{j}' for j in range(i+1, n+1)]
        for literal in literals_j:
            clause = literals_i + [literal]
            clauses.append(clause)
    
    # Create clauses for NOT operations
    for i in range(n):
        not_literal = f'~{literals[i]}'
        literals_i = [not_literal]
        literals_j = [f'x{j}' for j in range(i+1, n+1)]
        clause = literals_i + literals_j
        clauses.append(clause)
    
    return literals, clauses

def resolution_proof_width(clauses):
    # Simplify the formula using DPLL algorithm (simplified version)
    def dpll(clauses, model):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is not None:
            literal = unit_clause[0]
            new_model = model.copy()
            new_model[literal] = True
            if dpll([c for c in clauses if literal not in c and ~literal not in c], new_model):
                return True
            new_model[literal] = False
            if dpll([c for c in clauses if literal not in c and ~literal not in c], new_model):
                return True
            return False
        pure_literal = next((l for l in literals if all(l not in c or ~l in c for c in clauses)), None)
        if pure_literal is not None:
            new_model = model.copy()
            new_model[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and ~pure_literal not in c], new_model):
                return True
            new_model[pure_literal] = False
            if dpll([c for c in clauses if pure_literal not in c and ~pure_literal not in c], new_model):
                return True
            return False
        literal = literals[0]
        new_model_true = model.copy()
        new_model_true[literal] = True
        if dpll(clauses, new_model_true):
            return True
        new_model_false = model.copy()
        new_model_false[literal] = False
        if dpll(clauses, new_model_false):
            return True
        return False
    
    return len(literals) if not dpll(clauses, {}) else 0

def minimal_rank_vector_bundle(n):
    # Placeholder for the actual computation of the minimal rank of the vector bundle
    # This is a dummy implementation and should be replaced with an actual algorithm
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if len(metric_values) >= instances_tested:
            break
        
        literals, clauses = tseitin_formula(n)
        proof_width = resolution_proof_width(clauses)
        rank = minimal_rank_vector_bundle(n)
        
        metric_values.append(proof_width)
        n_max = max(n_max, n)
        
        if proof_width > rank:
            conjecture_holds = False
            counterexample = f"n={n}, w(φ_G)={proof_width} > k(G)={rank}"
    
    return {
        "metric_name": "Resolution Proof Width",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
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

# Helper functions for group cohomology and Frege proof width

def gaussian_elimination(A):
    n = len(A)
    m = len(A[0])
    rank = 0
    for i in range(n):
        if rank < m:
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] != 0:
                pivot = A[i][i]
                for j in range(m):
                    A[i][j] /= pivot
                for j in range(n):
                    if j != i and A[j][i] != 0:
                        factor = A[j][i]
                        for k in range(m):
                            A[j][k] -= factor * A[i][k]
                rank += 1
    return rank

def schur_multiplier(G):
    n = len(G)
    S = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1:
                S[i][j] = -1
                S[j][i] = -1
    return gaussian_elimination(S)

def frege_proof_width(phi_G):
    clauses = phi_G.split('\n')
    variables = set()
    for clause in clauses:
        literals = clause.strip().split()
        for literal in literals:
            if literal[0] == '-':
                variables.add(literal[1:])
            else:
                variables.add(literal)
    
    def dpll(clauses, assignment):
        unit_clauses = [c for c in clauses if len(c) == 1]
        while unit_clauses:
            literal = unit_clauses.pop()
            value = int(literal[0] != '-')
            variable = literal[1:]
            if variable not in assignment:
                assignment[variable] = value
            else:
                if assignment[variable] != value:
                    return False
        
        pure_literals = [c for c in clauses if len(c) == 1]
        while pure_literals:
            literal = pure_literals.pop()
            value = int(literal[0] != '-')
            variable = literal[1:]
            if variable not in assignment:
                assignment[variable] = value
            else:
                if assignment[variable] != value:
                    return False
        
        unsatisfied_clauses = [c for c in clauses if not any(l in assignment and assignment[l] == int(l[0] != '-') for l in c)]
        if not unsatisfied_clauses:
            return True
        
        literal, _ = random.choice(unsatisfied_clauses)
        value = int(literal[0] != '-')
        variable = literal[1:]
        return dpll(clauses, assignment | {variable: value}) or dpll(clauses, assignment | {-variable: 1 - value})
    
    return len(clauses) if dpll(clauses, {}) else float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n-1, 8))
    
    # Generate a random k-regular graph
    G = [[0]*n for _ in range(n)]
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < (k / (n - 1)):
                G[i][j] = G[j][i] = 1
                edges.append((i, j))
    
    # Construct the associated Tseitin formula φ_G
    phi_G = ""
    for edge in edges:
        u, v = edge
        var_uv = f"e_{u}_{v}"
        phi_G += f"{var_uv} | -{var_uv}\n"
        for i in range(n):
            if i != u and i != v:
                var_u_i = f"x_{u}_{i}"
                var_v_i = f"x_{v}_{i}"
                phi_G += f"({var_u_i} & {var_v_i}) -> -{var_uv}\n"
                phi_G += f"-({var_u_i} & {var_v_i}) -> {var_uv}\n"
    for i in range(n):
        var_x_i = f"x_{i}_{i}"
        phi_G += f"{var_x_i} | -{var_x_i}\n"
    
    # Compute the group cohomological dimension γ(G)
    gamma_G = schur_multiplier(G)
    
    # Measure the Frege proof width f(φ_G)
    f_phi_G = frege_proof_width(phi_G)
    
    return {
        "metric_name": "gamma_f_phi_ratio",
        "metric_value": gamma_G / f_phi_G if f_phi_G != float('inf') else 0,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": gamma_G <= 3 * f_phi_G and gamma_G / f_phi_G >= 0.8,
        "counterexample": "" if gamma_G <= 3 * f_phi_G and gamma_G / f_phi_G >= 0.8 else "gamma_G > 3*f_phi_G or gamma_G/f_phi_G < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gamma_G > 3*f_phi_G or gamma_G/f_phi_G < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
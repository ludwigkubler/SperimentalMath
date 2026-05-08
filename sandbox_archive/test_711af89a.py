# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]
    
    # Back-substitute to get solution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = A[i][n] / A[i][i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
    
    return x

def solve_linear_system(A, b):
    A_aug = [row + [b[i]] for i, row in enumerate(A)]
    solution = gaussian_elimination(A_aug)
    return solution

def generate_random_3regular_graph(n):
    edges = set()
    while len(edges) < n * 3 // 2:
        u, v = random.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    return list(edges)

def generate_dumbbell_graph():
    K4_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]
    bridge_edges = [(4, 5), (4, 6), (4, 7), (5, 8), (5, 9), (5, 10), (6, 8), (6, 9), (6, 10), (7, 8), (7, 9), (7, 10)]
    return K4_edges + bridge_edges

def generate_möbius_ladder_graph():
    n = 12
    edges = [(i, (i + 1) % n) for i in range(n)] + [(i, (i + n // 2) % n) for i in range(n)]
    return edges

def tseitin_formula(G, sigma):
    n = len(sigma)
    literals = {u: f"v{u}" for u in range(n)}
    neg_literals = {u: f"~v{u}" for u in range(n)}
    
    clauses = []
    for u in range(n):
        if sigma[u] == 1:
            clauses.append([literals[u]])
        else:
            clauses.append([-literals[u]])
    
    for (u, v) in G:
        clauses.append([neg_literals[u], literals[v]])
        clauses.append([neg_literals[v], literals[u]])
    
    return clauses

def dpll(clauses):
    def search(model):
        if not clauses:
            return model
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        pure_literals = defaultdict(int)
        for c in clauses:
            for l in c:
                pure_literals[l] += 1
        
        if unit_clauses:
            literal = unit_clauses[0]
            new_model = model + [literal]
            new_clauses = [[l for l in c if l != literal and l != -literal] for c in clauses]
            return search(new_model)
        
        if pure_literals:
            literal, count = max(pure_literals.items(), key=lambda x: abs(x[1]))
            new_model = model + [literal] if count > 0 else model + [-literal]
            new_clauses = [[l for l in c if l != literal and l != -literal] for c in clauses]
            return search(new_model)
        
        literal = next(iter(model))
        new_model_true = model + [literal]
        new_clauses_true = [[l for l in c if l != literal and l != -literal] for c in clauses]
        result_true = search(new_model_true)
        if result_true:
            return result_true
        
        new_model_false = model + [-literal]
        new_clauses_false = [[l for l in c if l != literal and l != -literal] for c in clauses]
        result_false = search(new_model_false)
        return result_false
    
    return search([])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 14, 16]
    results = []
    
    for n in n_values:
        for _ in range(30):
            if n == 8:
                G = generate_random_3regular_graph(n)
            elif n == 10:
                G = generate_dumbbell_graph()
            elif n == 12 or n == 14 or n == 16:
                G = generate_möbius_ladder_graph()
            else:
                raise ValueError("Invalid n value")
            
            sigma = [random.randint(0, 1) for _ in range(n)]
            if sum(sigma) % 2 != 1:
                continue
            
            phi_lp = float('inf')
            for d in range(1, n + 1):
                A = [[0] * (n * (n - 1) // 2) for _ in range(n * (n - 1) // 2)]
                b = [0] * (n * (n - 1) // 2)
                for i, u in enumerate(range(n)):
                    for j, v in enumerate(range(u + 1, n)):
                        if (u, v) in G:
                            A[i * (n - 1) // 2 + j][i * (n - 1) // 2 + j] = d
                            b[i * (n - 1) // 2 + j] += 1 / n
                try:
                    x = solve_linear_system(A, b)
                    phi_lp = min(phi_lp, sum(x))
                except Exception as e:
                    print(f"Error solving linear system for n={n}: {e}")
            
            nu = n * n * phi_lp
            
            clauses = tseitin_formula(G, sigma)
            T = len(dpll(clauses))
            
            results.append({
                "metric_name": "nu",
                "metric_value": nu,
                "instances_tested": 1,
                "conjecture_holds": log2(T) >= nu / 40 - 2,
                "counterexample": "" if log2(T) >= nu / 40 - 2 else f"n={n}, T={T}, nu={nu}"
            })
    
    mean_nu = sum(result["metric_value"] for result in results) / len(results)
    std_nu = math.sqrt(sum((result["metric_value"] - mean_nu) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_nu": mean_nu,
        "std_nu": std_nu,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_nu = sum(result["mean_nu"] for result in results) / len(results)
    std_nu = math.sqrt(sum((result["mean_nu"] - mean_nu) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if all(result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_nu} std={std_nu} support_fraction={support_fraction}")
    elif any(result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")
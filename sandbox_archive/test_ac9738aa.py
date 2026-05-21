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

def gaussian_elimination(matrix, b):
    n = len(matrix)
    augmented_matrix = [[matrix[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(augmented_matrix[k][i]) > abs(augmented_matrix[max_row][i]):
                max_row = k
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below pivot
        for k in range(i+1, n):
            factor = augmented_matrix[k][i] / augmented_matrix[i][i]
            for j in range(n + 1):
                augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (augmented_matrix[i][n] - sum(augmented_matrix[i][j] * x[j] for j in range(i+1, n))) / augmented_matrix[i][i]
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([3, 4, 5])
    num_clauses = n + 2
    clauses = [f"C{i}" for i in range(num_clauses)]
    variable_orderings = [[clauses[i] for i in random.sample(range(num_clauses), num_clauses)] for _ in range(30)]
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1 and c[0][0] != '-'), None)
        if unit_clause:
            literal = unit_clause[0]
            var = literal[1:]
            value = literal.startswith('-')
            assignment[var] = value
            return dpll([c for c in clauses if not any(lit in c for lit in (literal, f"-{var}"))], assignment)
        pure_literal = next((l for l in set(''.join(clause) for clause in clauses) if sum(1 for c in clauses if l in c) - sum(1 for c in clauses if f"-{l}" in c) == 0), None)
        if pure_literal:
            var = pure_literal[1:]
            value = pure_literal.startswith('-')
            assignment[var] = value
            return dpll([c for c in clauses if not any(lit in c for lit in (pure_literal, f"-{var}"))], assignment)
        literal = random.choice(random.choice(clauses))
        var = literal[1:]
        value = literal.startswith('-')
        assignment[var] = value
        return dpll([c for c in clauses if not any(lit in c for lit in (literal, f"-{var}"))], assignment) or dpll([c for c in clauses if not any(lit in c for lit in (f"-{literal}", f"{var}"))], {**assignment, var: not value})
    
    def build_complex(assignment):
        vertices = set(clauses)
        edges = []
        triangles = []
        
        for clause in clauses:
            for literal in clause:
                if literal[0] == '-':
                    continue
                other_clauses = [c for c in clauses if literal in c and literal != c[0]]
                for other_clause in other_clauses:
                    edges.append((literal, other_literal))
        
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                triangle = (clauses[i], clauses[j], f"{clauses[i]}{clauses[j]}")
                triangles.append(triangle)
        
        return vertices, edges, triangles
    
    def compute_betti_number(vertices, edges, triangles):
        n = len(vertices)
        m = len(edges)
        f = len(triangles)
        
        # Build boundary matrix ∂_2
        boundary_matrix = [[0] * (f + 1) for _ in range(m)]
        for i, (A, B, R) in enumerate(triangles):
            if A in edges and B in edges:
                boundary_matrix[edges.index(A)][i] = 1
                boundary_matrix[edges.index(B)][i] = -1
        
        # Compute rank of ∂_2
        rank_boundary = len(gaussian_elimination(boundary_matrix, [0] * (f + 1)))
        
        return m - n + len(vertices) - rank_boundary
    
    def compute_beta_ratio(beta_1, num_steps):
        return beta_1 / num_steps
    
    results = []
    for ordering in variable_orderings:
        assignment = {}
        if dpll(clauses, assignment):
            vertices, edges, triangles = build_complex(assignment)
            beta_1 = compute_betti_number(vertices, edges, triangles)
            num_steps = len(edges) + len(triangles)
            beta_ratio = compute_beta_ratio(beta_1, num_steps)
            results.append((beta_1, beta_ratio))
    
    if not results:
        return {
            "metric_name": "β_1(K(P);F_2)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    beta_1_values = [beta for beta, _ in results]
    beta_ratio_values = [ratio for _, ratio in results]
    
    if any(beta < math.floor(n * math.log2(n + 1)) for beta, _ in results):
        return {
            "metric_name": "β_1(K(P);F_2)",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"β_1 < {math.floor(n * math.log2(n + 1))}"
        }
    
    mean_beta_1 = sum(beta_1_values) / len(beta_1_values)
    mean_beta_ratio = sum(beta_ratio_values) / len(beta_ratio_values)
    var_beta_ratio = sum((ratio - mean_beta_ratio)**2 for ratio in beta_ratio_values) / len(beta_ratio_values)
    
    return {
        "metric_name": "β_1(K(P);F_2)",
        "metric_value": mean_beta_1,
        "instances_tested": len(results),
        "conjecture_holds": mean_beta_ratio > 0.01 and var_beta_ratio <= (sum((ratio - mean_beta_ratio)**2 for ratio in beta_ratio_values[:3]) / 3) if n == 5 else True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_beta_1 = sum(r["metric_value"] for r in results) / len(results)
        var_beta_ratio_n3 = sum((r["beta_ratio_values"][0] - (sum(r["beta_ratio_values"][:3]) / 3))**2 for r in results if "beta_ratio_values" in r and len(r["beta_ratio_values"]) >= 3) / len(results)
        var_beta_ratio_n5 = sum((r["beta_ratio_values"][1] - (sum(r["beta_ratio_values"][:3]) / 3))**2 for r in results if "beta_ratio_values" in r and len(r["beta_ratio_values"]) >= 3) / len(results)
        support_fraction = sum("conjecture_holds" in r and r["conjecture_holds"] for r in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_beta_1} std={var_beta_ratio_n5} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")
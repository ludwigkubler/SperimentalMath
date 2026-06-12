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
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        det *= A[i][i]
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        # Generate a random Boolean formula with n clauses
        num_variables = n + 1
        literals = list(range(-num_variables, 0)) + list(range(1, num_variables + 1))
        formula = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            formula.append(clause)
        
        # Construct the Tseitin formula φ_F
        tseitin_vars = list(range(1, n + num_variables + 1))
        tseitin_clauses = []
        for i, clause in enumerate(formula):
            tseitin_clauses.append([tseitin_vars[i], -clause[0]])
            tseitin_clauses.append([tseitin_vars[i], -clause[1]])
            tseitin_clauses.append([-tseitin_vars[i], clause[0], clause[1]])
        tseitin_clauses.append([tseitin_vars[n + num_variables]])
        for i in range(n):
            tseitin_clauses.append([-tseitin_vars[n + num_variables], tseitin_vars[i]])
        
        # Compute the resolution proof width w(φ_F)
        def resolve(clauses, resolvents):
            new_resolvents = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 2:
                        new_clause = list(set(clause1 + clause2) - {list(set(clause1) & set(clause2))[0]})
                        if new_clause not in resolvents and new_clause not in clauses:
                            new_resolvents.append(new_clause)
            return new_resolvents
        
        def resolution_width(clauses):
            resolvents = []
            while True:
                new_resolvents = resolve(clauses, resolvents)
                if not new_resolvents:
                    break
                resolvents.extend(new_resolvents)
                clauses.extend(resolvents)
            return len(set([tuple(sorted(c)) for c in clauses]))
        
        w_phi_F = resolution_width(tseitin_clauses)
        
        # Compute the clause entanglement graph G_F and derive the quadratic form Q(F)
        def clause_entanglement_graph(formula):
            graph = {i: [] for i in range(n)}
            for i, clause in enumerate(formula):
                for j, other_clause in enumerate(formula[i+1:], start=i+1):
                    if len(set(clause) & set(other_clause)) == 2:
                        graph[i].append(j)
                        graph[j].append(i)
            return graph
        
        def quadratic_form(graph):
            n = len(graph)
            A = [[0] * n for _ in range(n)]
            for i, neighbors in enumerate(graph):
                for j in neighbors:
                    A[i][j] += 1
                    A[j][i] += 1
            gaussian_elimination(A)
            norm = sum(abs(x) for row in A for x in row if x != 0)
            return norm
        
        Q_F = quadratic_form(clause_entanglement_graph(formula))
        
        # Measure the metric
        instances_tested += 1
        metric_values.append(Q_F)
        
        # Check correlation
        if len(metric_values) > 1:
            mean_metric = sum(metric_values) / len(metric_values)
            variance = sum((x - mean_metric) ** 2 for x in metric_values) / (len(metric_values) - 1)
            std_dev = math.sqrt(variance)
            z_score = (mean_metric - w_phi_F) / std_dev
            p_value = 2 * (1 - 0.5 * (1 + math.erf(z_score / math.sqrt(2))))
            if p_value < 0.05:
                conjecture_holds = False
                counterexample = f"Failed at n={n}, Q(F)={Q_F}, w(φ_F)={w_phi_F}"
    
    return {
        "metric_name": "minimal_norm",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
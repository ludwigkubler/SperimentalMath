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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_regular_graph(n, k):
        if (k * n) % 2 != 0 or k >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < k * n // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        num_vars = 2 * n + n * (n - 1) // 2
        clauses = []
        literals = list(range(1, num_vars + 1))
        
        for i in range(n):
            clauses.append([literals[i], literals[n + i]])
            clauses.append([-literals[i], -literals[n + i]])
        
        for u in range(n):
            for v in graph[u]:
                if u < v:
                    clauses.append([literals[u * (n - 1) // 2 + v], literals[v * (n - 1) // 2 + u]])
                    clauses.append([-literals[u * (n - 1) // 2 + v], -literals[v * (n - 1) // 2 + u]])
        
        return clauses

    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                matrix[i][j] /= matrix[i][i]
            matrix[i][i] = 1
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def group_cohomological_dimension(graph):
        n = len(graph)
        if n <= 1:
            return 0
        edges = set()
        for u in range(n):
            for v in graph[u]:
                if (u, v) not in edges and (v, u) not in edges:
                    edges.add((u, v))
        m = len(edges)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, (u, v) in enumerate(edges):
            A[i][u] = 1
            A[i][v] = -1
            A[i][n] = 1
        
        reduced_A = gaussian_elimination(A)
        if not reduced_A:
            return float('inf')
        
        rank = sum(1 for row in reduced_A if any(row[j] != 0 for j in range(n + 1)))
        return n - rank

    def frege_proof_width(clauses):
        def dpll(clauses, assignment):
            unsatisfied_clauses = [c for c in clauses if not any(l in assignment and (l > 0) == (assignment[l] > 0) for l in c)]
            if not unsatisfied_clauses:
                return True
            unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                assignment[literal] = 1 if literal > 0 else -1
                return dpll(clauses, assignment)
            
            literal = random.choice([c for c in unsatisfied_clauses[0] if c != 0])
            return dpll(clauses, assignment | {literal}) or dpll(clauses, assignment | {-literal})
        
        return len(clauses) if dpll(clauses, {}) else float('inf')

    def generate_random_clause(num_vars):
        clause = []
        for _ in range(random.randint(1, num_vars)):
            literal = random.choice([-i for i in range(1, num_vars + 1)] + [i for i in range(1, num_vars + 1)])
            if literal not in clause:
                clause.append(literal)
        return clause

    def generate_random_clauses(num_vars, num_clauses):
        clauses = []
        while len(clauses) < num_clauses:
            clause = generate_random_clause(num_vars)
            if clause and all(c not in clauses for c in [tuple(sorted(c)) for c in clauses]):
                clauses.append(tuple(sorted(clause)))
        return clauses

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_k_regular_graph(n, 2)
        if not graph:
            continue
        phi_G = tseitin_formula(graph)
        gamma_G = group_cohomological_dimension(graph)
        f_phi_G = frege_proof_width(phi_G)
        
        results.append({
            "n": n,
            "gamma_G": gamma_G,
            "f_phi_G": f_phi_G
        })

    if not results:
        return {
            "metric_name": "group_cohomological_dimension",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    gamma_values = [r["gamma_G"] for r in results]
    f_phi_values = [r["f_phi_G"] for r in results]
    
    correlation_coefficient = sum((gamma_values[i] - mean(gamma_values)) * (f_phi_values[i] - mean(f_phi_values)) for i in range(len(results))) / len(results)
    if math.isnan(correlation_coefficient):
        correlation_coefficient = 0
    
    support_fraction = sum(1 for r in results if r["gamma_G"] <= 3 * r["f_phi_G"]) / len(results)
    
    return {
        "metric_name": "group_cohomological_dimension",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": support_fraction >= 0.8 and correlation_coefficient >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"correlation_coefficient={correlation_coefficient}, gamma_G > 3 * f_phi_G"
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = mean([r["metric_value"] for r in results if r["instances_tested"] > 0])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")
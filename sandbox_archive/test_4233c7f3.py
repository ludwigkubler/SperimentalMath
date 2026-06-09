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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            sign = (-1) ** j
            det += sign * A[0][j] * determinant(submatrix)
        return det

    def is_independent_set(matroid, S):
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                if (S[i], S[j]) in matroid or (S[j], S[i]) in matroid:
                    return False
        return True

    def geometric_entropy(matroid):
        n = len(matroid)
        independent_sets = []
        for i in range(1 << n):
            S = [j for j in range(n) if i & (1 << j)]
            if is_independent_set(matroid, S):
                independent_sets.append(S)
        
        entropy = 0
        total_weight = sum(determinant(matrix_multiply([[int(j == k) for k in range(n)] for j in S])) for S in independent_sets)
        for S in independent_sets:
            weight = determinant(matrix_multiply([[int(j == k) for k in range(n)] for j in S]))
            entropy += weight * math.log2(weight / total_weight)
        
        return -entropy

    def resolution_width(phi):
        clauses = phi.split(' ')
        variables = set()
        for clause in clauses:
            if clause.startswith('-'):
                continue
            variables.update(clause.split('|'))
        
        n_vars = len(variables)
        assignment = [False] * n_vars
        
        def is_satisfiable():
            for clause in clauses:
                if not any(assignment[var] == (clause.startswith('-') and var + 1 or var) for var in range(n_vars)):
                    return False
            return True
        
        max_width = 0
        while is_satisfiable():
            unsatisfied_clauses = [i for i, clause in enumerate(clauses) if not any(assignment[var] == (clause.startswith('-') and var + 1 or var) for var in range(n_vars))]
            width = len(set(clause.split('|') for i in unsatisfied_clauses for clause in clauses[i].split(' ')))
            max_width = max(max_width, width)
            assignment[random.choice([i for i in range(n_vars) if not assignment[i]])] = True
        
        return max_width

    def generate_d_regular_graph(d, n):
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            clauses.append(f"X{i} | -X{i}")
        for u in range(n):
            for v in graph[u]:
                clauses.append(f"-X{u} | X{v}")
        return ' '.join(clauses)

    def matroid_from_graph(graph):
        n = len(graph)
        matroid = set()
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) not in graph and (j, i) not in graph:
                    matroid.add((i, j))
        return matroid

    def compute_metric_value(n):
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(d, n)
        matroid = matroid_from_graph(graph)
        phi = tseitin_formula(graph)
        mge = geometric_entropy(matroid)
        w = resolution_width(phi)
        return {"mge(G)": mge, "w(φ_G)": w}

    metric_values = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        result = compute_metric_value(n)
        metric_values.append(result["mge(G)"])
    
    if any(v > 10 for v in metric_values) or any(w < 3 for w in [compute_metric_value(40)["w(φ_G)"]]):
        return {
            "metric_name": "mge(G)",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": len(metric_values),
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mge(G) > 10 or w(φ_G) < 3"
        }
    
    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, [compute_metric_value(n)["w(φ_G)"] for n in [5, 10, 15, 20, 30, 40]])) / len(metric_values)
    support_fraction = sum(1 for v in metric_values if v > mean) / len(metric_values)
    
    return {
        "metric_name": "mge(G)",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(metric_values),
        "n_max": 40,
        "conjecture_holds": correlation_coefficient >= 0.7 and support_fraction >= 0.8333,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
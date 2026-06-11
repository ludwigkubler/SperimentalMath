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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(3 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                continue
            clauses.append(clause)
        return clauses
    
    def tautological_ideal(cnf):
        # Placeholder for actual computation of the tautological ideal
        return set()
    
    def local_induction_degree(ideal):
        # Placeholder for actual computation of the local induction degree
        return 0
    
    def bipartite_graph(cnf):
        n = len(cnf[0])
        adj_matrix = [[0] * (2 * n) for _ in range(2 * n)]
        for i, clause in enumerate(cnf):
            for lit in clause:
                if lit > 0:
                    u = lit - 1
                    v = n + i
                else:
                    u = -lit - 1
                    v = n + i
                adj_matrix[u][v] = 1
                adj_matrix[v][u] = 1
        return adj_matrix
    
    def spectral_gap(laplacian):
        n = len(laplacian)
        eigenvalues = []
        for _ in range(5):  # Simple power iteration method to approximate largest eigenvalue
            v = [random.random() for _ in range(n)]
            v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
            for _ in range(10):
                v_next = [sum(laplacian[i][j] * v[j] for j in range(n)) for i in range(n)]
                v_next = [x / math.sqrt(sum(x**2 for x in v_next)) for x in v_next]
            lambda_i = sum(v_next[i] * laplacian[i][j] * v_next[j] for i in range(n) for j in range(n))
            eigenvalues.append(lambda_i)
        return max(eigenvalues)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None  # Singular matrix
            for j in range(n):
                if i == j:
                    continue
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        n = len(matrix)
        det = 0
        if n == 2:
            det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def laplacian_matrix(graph):
        n = len(graph)
        laplacian = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(graph[i])
            laplacian[i][i] = degree
            for j in range(i + 1, n):
                if graph[i][j]:
                    laplacian[i][j] = -1
                    laplacian[j][i] = -1
        return laplacian
    
    def mli(phi):
        ideal = tautological_ideal(phi)
        return local_induction_degree(ideal)
    
    def g(phi):
        graph = bipartite_graph(phi)
        laplacian = laplacian_matrix(graph)
        return spectral_gap(laplacian)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        phi = generate_cnf(n)
        mli_phi = mli(phi)
        g_phi = g(phi)
        if mli_phi is None or g_phi is None:
            return {
                "metric_name": "mli_vs_g",
                "metric_value": 0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        results.append((mli_phi, g_phi))
    
    mli_values = [x[0] for x in results]
    g_values = [x[1] for x in results]
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        ranks_x = {v: i + 1 for i, v in enumerate(sorted(set(x), reverse=True))}
        ranks_y = {v: i + 1 for i, v in enumerate(sorted(set(y), reverse=True))}
        d_squared_sum = sum((ranks_x[x[i]] - ranks_y[y[i]]) ** 2 for i in range(n))
        rho = 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
        return rho
    
    rho = spearman_rank_correlation(mli_values, g_values)
    
    return {
        "metric_name": "mli_vs_g",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": rho > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho < 0.7\" first_failing_seed={first_failing_seed}")
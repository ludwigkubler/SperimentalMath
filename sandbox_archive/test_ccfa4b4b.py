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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d >= n:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < d * n // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and adj_matrix[u][v] == 0:
                adj_matrix[u][v] = 1
                adj_matrix[v][u] = 1
                edges_added += 1
        return adj_matrix

    def zonotope_construction(adj_matrix):
        n = len(adj_matrix)
        vertices = []
        for i in range(n):
            vertex = [0] * n
            vertex[i] = 1
            vertices.append(vertex)
            vertex[i] = -1
            vertices.append(vertex)
        return vertices

    def ehrhart_rank(vertices):
        n = len(vertices[0])
        count = 0
        for i in range(2**n):
            point = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    point[j] = 1
            if all(all(point[k] + vertices[m][k] >= 0 for k in range(n)) for m in range(len(vertices))):
                count += 1
        return count

    def sat_clause_depth(adj_matrix):
        n = len(adj_matrix)
        clauses = []
        for i in range(n):
            clause = [i]
            for j in range(i+1, n):
                if adj_matrix[i][j] == 1:
                    clause.append(j)
            clauses.append(clause)
        return len(clauses)

    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x_i - mean_x) * (y_i - mean_y) for x_i, y_i in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((x_i - mean_x)**2 for x_i in x) / len(x))
        std_y = math.sqrt(sum((y_i - mean_y)**2 for y_i in y) / len(y))
        return cov_xy / (std_x * std_y)

    n_values = [5, 10, 15, 20, 30, 40]
    m_Ehr_values = []
    c_G_values = []

    for n in n_values:
        G = generate_d_regular_graph(n, 2)
        if G is None:
            continue
        P_G = zonotope_construction(G)
        m_Ehr = ehrhart_rank(P_G)
        c_G = sat_clause_depth(G)
        m_Ehr_values.append(m_Ehr)
        c_G_values.append(c_G)

    if len(m_Ehr_values) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(m_Ehr_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    r = correlation_coefficient(m_Ehr_values, c_G_values)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": r,
        "instances_tested": len(m_Ehr_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(r) >= 0.99,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient' first_failing_seed={first_failing_seed}")
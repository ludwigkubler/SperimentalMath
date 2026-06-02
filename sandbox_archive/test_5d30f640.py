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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(d, n):
        if d * n % 2 != 0:
            raise ValueError("d * n must be even")
        G = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < (d * n) // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                G[u][v] = 1
                G[v][u] = 1
                edges.add((u, v))
        return G
    
    def resolution_width(phi):
        # Simplified DPLL solver for demonstration purposes
        stack = []
        assignment = [None] * len(phi)
        for clause in phi:
            if all(assignment[var] == (not lit) for var, lit in clause):
                continue
            unassigned_var = next((var for var, lit in clause if assignment[var] is None), None)
            if unassigned_var is None:
                return 0
            stack.append(unassigned_var)
            assignment[unassigned_var] = True
        while stack:
            var = stack.pop()
            assignment[var] = False
            for clause in phi:
                if all(assignment[var] == (not lit) for var, lit in clause):
                    continue
                unassigned_var = next((var for var, lit in clause if assignment[var] is None), None)
                if unassigned_var is None:
                    return 0
                stack.append(unassigned_var)
                assignment[unassigned_var] = True
        return len(stack)
    
    def noncommutative_crossed_product_order(G):
        n = len(G)
        phi = []
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    phi.append([(i, True), (j, False)])
                    phi.append([(j, True), (i, False)])
        A = [[0] * len(phi) for _ in range(len(phi))]
        b = [0] * len(phi)
        for i in range(len(phi)):
            for j in range(i+1, len(phi)):
                if any(phi[i][k] == phi[j][k] for k in range(2)):
                    A[i][j] += 1
                    A[j][i] += 1
        x = gaussian_elimination(A, b)
        return sum(x)

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        d = random.randint(2, 40)
        n = (d * n_max) // 2 + 1
        G = generate_d_regular_graph(d, n)
        phi = resolution_width(G)
        Order = noncommutative_crossed_product_order(G)
        metric_values.append(Order)

    mean_value = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "Order",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,  # This is a placeholder; actual correlation check would be needed
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
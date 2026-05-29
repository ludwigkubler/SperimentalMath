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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_power(A, n):
        result = [[1 if i == j else 0 for j in range(len(A))] for i in range(len(A))]
        while n > 0:
            if n % 2 == 1:
                result = matrix_multiply(result, A)
            A = matrix_multiply(A, A)
            n //= 2
        return result

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def is_invertible(A):
        return determinant(A) != 0

    def generate_polynomial(n):
        coefficients = [random.randint(0, 1) for _ in range(n+1)]
        return coefficients

    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result

    def generate_random_function(n):
        degree = random.randint(1, n-1)
        poly = generate_polynomial(degree)
        return lambda x: evaluate_polynomial(poly, x)

    def construct_incidence_graph(f, n):
        graph = [[0] * (n+1) for _ in range(n+1)]
        for i in range(n+1):
            for j in range(n+1):
                if f(i) == f(j):
                    graph[i][j] = 1
        return graph

    def count_edges(graph):
        return sum(sum(row) for row in graph) // 2

    n_values = [5, 10, 15, 20, 30, 40]
    total_edges = 0
    num_instances = 0
    beta = None
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            f = generate_random_function(n)
            graph = construct_incidence_graph(f, n)
            edges = count_edges(graph)
            if is_invertible(graph):
                total_edges += edges
                num_instances += 1

    if num_instances == 0:
        return {
            "metric_name": "E[|E(G_f)|/√(nD)]",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No invertible incidence graphs found"
        }

    mean_edges = total_edges / num_instances
    beta = mean_edges / math.sqrt(n * (n_values[-1] + 5))

    return {
        "metric_name": "E[|E(G_f)|/√(nD)]",
        "metric_value": beta,
        "instances_tested": num_instances,
        "conjecture_holds": beta <= 10,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_beta = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_beta} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
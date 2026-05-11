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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    result = [[0.0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def transpose(A):
    return [list(row) for row in zip(*A)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses

    def hypergraph_to_adjacency_list(hypergraph):
        adj_list = [[] for _ in range(len(hypergraph))]
        for edge in hypergraph:
            for node in edge:
                if node not in adj_list[edge[0]]:
                    adj_list[edge[0]].append(node)
                if node not in adj_list[edge[1]]:
                    adj_list[edge[1]].append(node)
        return adj_list

    def cheeger_constant(adj_list):
        n = len(adj_list)
        lambda_min = float('inf')
        for i in range(n):
            degrees = [len(neighbors) for neighbors in adj_list]
            adjacency_matrix = [[0] * n for _ in range(n)]
            for j in range(n):
                for k in range(j + 1, n):
                    if k in adj_list[j]:
                        adjacency_matrix[j][k] = 1
                        adjacency_matrix[k][j] = 1
            laplacian = [[0] * n for _ in range(n)]
            for j in range(n):
                laplacian[j][j] = degrees[j]
                for k in range(j + 1, n):
                    laplacian[j][k] = -adjacency_matrix[j][k]
                    laplacian[k][j] = -adjacency_matrix[k][j]
            eigenvalues = sorted(gaussian_elimination(laplacian, [0] * n))
            lambda_min = min(lambda_min, eigenvalues[1])
        return lambda_min / max(degrees)

    def dpll(clauses):
        if not clauses:
            return 1
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_clauses = []
            for clause in clauses:
                if literal not in clause and -literal not in clause:
                    new_clauses.append(clause)
                elif literal in clause:
                    continue
                else:
                    new_clause = [l for l in clause if l != -literal]
                    new_clauses.append(new_clause)
            return dpll(new_clauses) * 2
        pure_literals = set()
        for clause in clauses:
            literals = set(clause)
            if len(literals.intersection(pure_literals)) == 0 and len(literals.intersection(-pure_literals)) == 0:
                pure_literals.update(literals)
        if not pure_literals:
            return dpll([c[:] for c in clauses])
        literal = next(iter(pure_literals))
        new_clauses = []
        for clause in clauses:
            if literal not in clause and -literal not in clause:
                new_clauses.append(clause)
            elif literal in clause:
                continue
            else:
                new_clause = [l for l in clause if l != -literal]
                new_clauses.append(new_clause)
        return dpll(new_clauses) * 2

    for _ in range(100):
        hypergraph = generate_3cnf(n)
        adj_list = hypergraph_to_adjacency_list(hypergraph)
        h_phi = cheeger_constant(adj_list)
        size_pi = dpll(hypergraph)
        instances_tested += 1
        total_metric_value += h_phi * size_pi
        if h_phi * size_pi > 1:
            conjecture_holds = False
            counterexample = f"n={n}, h(Φ)={h_phi}, size(Π)={size_pi}"

    metric_name = "h(Φ) * size(Π)"
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 1.0 if conjecture_holds else 0.0

    return {
        "metric_name": metric_name,
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")
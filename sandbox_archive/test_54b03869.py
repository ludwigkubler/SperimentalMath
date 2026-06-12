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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(M, mod):
    n = len(M)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = M[i][i]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
        factor = mod_inverse(pivot, mod)
        for j in range(n):
            M[i][j] = (M[i][j] * factor) % mod
            I[i][j] = (I[i][j] * factor) % mod
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(n):
                    M[k][j] = (M[k][j] - factor * M[i][j]) % mod
                    I[k][j] = (I[k][j] - factor * I[i][j]) % mod
    return I

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_pow(M, p, mod):
    n = len(M)
    result = [[int(i == j) for j in range(n)] for i in range(n)]
    while p > 0:
        if p % 2 == 1:
            result = matrix_mul(result, M, mod)
        M = matrix_mul(M, M, mod)
        p //= 2
    return result

def binomial_coefficient(n, k):
    if k > n:
        return 0
    num = math.factorial(n)
    den = math.factorial(k) * math.factorial(n - k)
    return num // den

def gaussian_elimination(A, b, mod):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] = (A[i][j] * mod_inverse(pivot, mod)) % mod
        b[i] = (b[i] * mod_inverse(pivot, mod)) % mod
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % mod
                b[j] = (b[j] - factor * b[i]) % mod
    return [b[i] for i in range(n)]

def generate_cnf(n):
    clauses = []
    for _ in range(2 ** n):
        clause = [random.randint(-1, 0) * random.randint(1, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def construct_birational_variety(cnf):
    n = len(cnf[0])
    A = [[0 for _ in range(n)] for _ in range(n)]
    b = [0 for _ in range(n)]
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                A[literal - 1][literal - 1] += 1
            else:
                A[-literal - 1][-literal - 1] += 1
        b[abs(literal) - 1] += 1
    return A, b

def minimal_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if any(A[j][i] != 0 for j in range(i, n)):
            rank += 1
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
    return rank

def clause_tree_width(cnf):
    n = len(cnf[0])
    graph = [[] for _ in range(2 * n)]
    for i, clause in enumerate(cnf):
        for literal in clause:
            if literal > 0:
                graph[literal - 1].append(n + i)
                graph[n + i].append(literal - 1)
            else:
                graph[-literal - 1].append(n + i)
                graph[n + i].append(-literal - 1)
    queue = [i for i in range(2 * n) if len(graph[i]) == 1]
    visited = set(queue)
    while queue:
        node = queue.pop()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return len(visited)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    for n in n_values:
        cnf = generate_cnf(n)
        A, b = construct_birational_variety(cnf)
        rank = minimal_rank(A)
        width = clause_tree_width(cnf)
        ranks.append(rank)
        widths.append(width)
    
    if len(ranks) < 30 or len(widths) < 30:
        return {
            "metric_name": "minimal_rank_vs_clause_tree_width",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = 0
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    for rank, width in zip(ranks, widths):
        correlation += (rank - mean_rank) * (width - mean_width)
    correlation /= math.sqrt(sum((x - mean_rank) ** 2 for x in ranks)) * math.sqrt(sum((y - mean_width) ** 2 for y in widths))
    
    mae = sum(abs(rank - width) for rank, width in zip(ranks, widths)) / len(ranks)
    
    return {
        "metric_name": "minimal_rank_vs_clause_tree_width",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mae <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
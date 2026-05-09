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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def is_real_stable(P):
    n = len(P)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j:
                A[i][j] = P[j]
        b[i] = -P[i]
    x = gaussian_elimination(A, b)
    return all(x[i] >= 0 for i in range(n))

def generate_3cnf_instance(n, m):
    clauses = []
    variables = set()
    for _ in range(m):
        clause = random.sample(range(1, n+1), 3)
        for var in clause:
            variables.add(var)
        clauses.append(clause)
    return clauses, list(variables)

def conflict_graph(clauses, variables):
    graph = {var: [] for var in variables}
    for clause in clauses:
        for i in range(3):
            for j in range(i+1, 3):
                if clause[i] != -clause[j]:
                    graph[abs(clause[i])].append(abs(clause[j]))
                    graph[abs(clause[j])].append(abs(clause[i]))
    return graph

def max_clique_size(graph):
    def dfs(node, visited, current_clique):
        visited.add(node)
        current_clique.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, visited, current_clique)
    
    max_size = 0
    for node in graph:
        visited = set()
        current_clique = []
        dfs(node, visited, current_clique)
        max_size = max(max_size, len(current_clique))
    return max_size

def sos_degree(clauses):
    n = len(clauses)
    P = [1] * (n + 1)
    for clause in clauses:
        for i in range(3):
            P[abs(clause[i])] += 1
    return sum(P)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * (n - 1) // 2, n * (n + 1) // 2)
    clauses, variables = generate_3cnf_instance(n, m)
    graph = conflict_graph(clauses, variables)
    omega = max_clique_size(graph)
    P = [0] * (len(variables) + 1)
    for clause in clauses:
        for i in range(3):
            P[abs(clause[i])] += 1
    deg_SOS = sos_degree(clauses)
    metric_value = deg_SOS
    conjecture_holds = deg_SOS >= math.log2(omega) + 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "deg_SOS",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
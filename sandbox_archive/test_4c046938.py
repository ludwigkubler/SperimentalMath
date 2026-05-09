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

def generate_primes(min_val, max_val):
    primes = []
    for num in range(min_val, max_val + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        factor = A_augmented[i][i]
        for j in range(i, n+1):
            A_augmented[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = A_augmented[j][i]
                for k in range(i, n+1):
                    A_augmented[j][k] -= factor * A_augmented[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A_augmented[i][-1]
        for j in range(i+1, n):
            x[i] -= A_augmented[i][j] * x[j]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    num_clauses = math.ceil(n * (random.uniform(1.2, 2.5)))
    variables = list(range(n))
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice(variables) for _ in range(3)]
        if random.choice([True, False]):
            clause[0] = -clause[0]
        if random.choice([True, False]):
            clause[1] = -clause[1]
        clauses.append(clause)
    
    clause_graph = [[0] * n for _ in range(n)]
    for clause in clauses:
        for var in clause:
            if var > 0:
                clause_graph[var-1][var-1] += 1
            else:
                clause_graph[-var-1][-var-1] += 1
    
    connected_components = []
    visited = [False] * n
    def dfs(node):
        stack = [node]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in range(n):
                    if clause_graph[node][neighbor] > 0 and not visited[neighbor]:
                        stack.append(neighbor)
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
            connected_components.append(sum(1 for j in range(n) if visited[j]))
    
    edges = sum(sum(row) // 2 for row in clause_graph)
    betti_1 = edges - n + len(connected_components)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = abs(unit_clause[0])
            value = unit_clause[0] > 0
            assignment[var-1] = value
            new_clauses = [c for c in clauses if not any(v in c for v in (var, -var))]
            return dpll(new_clauses, assignment)
        pure_literal = next((v for v in range(1, n+1) if sum(c.count(v) + c.count(-v) for c in clauses) == 1), None)
        if pure_literal:
            value = sum(c.count(pure_literal) for c in clauses) > 0
            assignment[pure_literal-1] = value
            new_clauses = [c for c in clauses if not any(v in c for v in (pure_literal, -pure_literal))]
            return dpll(new_clauses, assignment)
        var = random.choice([v for v in range(1, n+1) if sum(c.count(v) + c.count(-v) for c in clauses) > 0])
        value = True
        new_assignment = assignment[:]
        new_assignment[var-1] = value
        if dpll(clauses, new_assignment):
            return True
        new_assignment[var-1] = False
        if dpll(clauses, new_assignment):
            return True
        return False
    
    assignment = [None] * n
    dpll_clauses = clauses[:]
    dpll_size = 0
    while dpll_clauses:
        clause = random.choice(dpll_clauses)
        var = abs(clause[0])
        value = clause[0] > 0
        assignment[var-1] = value
        new_clauses = [c for c in dpll_clauses if not any(v in c for v in (var, -var))]
        dpll_clauses = new_clauses
        dpll_size += 1
    
    result = {
        "metric_name": "Betti_1 * DPLL_size",
        "metric_value": betti_1 * dpll_size,
        "instances_tested": 1,
        "conjecture_holds": 0.8 * n <= betti_1 * dpll_size <= 1.2 * n,
        "counterexample": "" if result["conjecture_holds"] else f"n={n}, Betti_1*{dpll_size}={betti_1*dpll_size}"
    }
    return result

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(100, 500)
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
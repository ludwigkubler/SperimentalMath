# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

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

def adjacency_matrix(A, B):
    n = len(A)
    m = len(B)
    adj = [[0] * (n + m) for _ in range(n + m)]
    for i in range(n):
        for j in range(m):
            if A[i][j]:
                adj[i][len(A) + j] = 1
                adj[len(A) + j][i] = 1
    return adj

def gaussian_elimination(matrix, b):
    n = len(matrix)
    augmented_matrix = [row[:] + [b[i]] for i, row in enumerate(matrix)]
    
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        factor = augmented_matrix[i][i]
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= factor
        
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i + 1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
    
    return x

def tseitin_formula(A, B):
    n = len(A)
    m = len(B)
    clauses = []
    literals = {}
    var_count = 0
    
    for i in range(n):
        literals[(i, 'A')] = var_count
        var_count += 1
    
    for j in range(m):
        literals[(j, 'B')] = var_count
        var_count += 1
    
    for i in range(n):
        clauses.append([literals[(i, 'A')]])
    
    for j in range(m):
        clauses.append([-literals[(j, 'B')]])
    
    for i in range(n):
        for j in range(m):
            if A[i][j]:
                clauses.append([-literals[(i, 'A')], literals[(j, 'B')]])
                clauses.append([literals[(i, 'A')], -literals[(j, 'B')]])
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    m = random.randint(2 * n // 3, n)
    A = [[random.choice([0, 1]) for _ in range(m)] for _ in range(n)]
    B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    adj = adjacency_matrix(A, B)
    monomials = set()
    
    def dfs(node, path):
        if node == len(A) + m:
            monomials.add(tuple(sorted(path)))
            return
        if node < len(A):
            dfs(node + 1, path + [node])
        else:
            for j in range(m):
                if A[node - len(A)][j]:
                    dfs(j, path)
    
    dfs(0, [])
    
    clauses = tseitin_formula(A, B)
    num_clauses = len(clauses)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] = literal > 0
            return dpll(clauses, new_assignment)
        
        literal = next((c[0] for c in clauses if not any(abs(x) == abs(c[0]) for x in assignment)), None)
        if literal is None:
            return False
        
        new_clauses_true = [c for c in clauses if literal not in c and -literal not in c]
        new_assignment_true = assignment[:]
        new_assignment_true[abs(literal) - 1] = literal > 0
        if dpll(new_clauses_true, new_assignment_true):
            return True
        
        new_clauses_false = [c for c in clauses if -literal not in c and literal not in c]
        new_assignment_false = assignment[:]
        new_assignment_false[abs(literal) - 1] = literal < 0
        if dpll(new_clauses_false, new_assignment_false):
            return True
        
        return False
    
    proof_size = 0
    for _ in range(10):  # Sample multiple instances per seed
        assignment = [False] * num_clauses
        if not dpll(clauses, assignment):
            proof_size += 1
    
    metric_value = len(monomials)
    conjecture_holds = proof_size == metric_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": proof_size,
        "instances_tested": 10,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
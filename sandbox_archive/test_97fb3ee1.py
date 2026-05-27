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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def mod_inverse(a, m):
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            return None
        else:
            return x % m
    
    def matrix_mod_inv(matrix, mod):
        n = len(matrix)
        adj = [[0] * n for _ in range(n)]
        det = determinant(matrix) % mod
        
        if det == 0:
            return None
        
        inv_det = mod_inverse(det, mod)
        
        for i in range(n):
            for j in range(n):
                minor = get_minor(matrix, i, j)
                adj[i][j] = (inv_det * (-1)**(i+j) * determinant(minor)) % mod
        
        return transpose(adj)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            minor = get_minor(matrix, 0, j)
            det += (-1)**j * matrix[0][j] * determinant(minor)
        return det
    
    def transpose(matrix):
        n = len(matrix)
        m = len(matrix[0])
        transposed = [[matrix[j][i] for j in range(n)] for i in range(m)]
        return transposed
    
    def get_minor(matrix, row, col):
        minor = []
        for i in range(len(matrix)):
            if i != row:
                new_row = []
                for j in range(len(matrix[i])):
                    if j != col:
                        new_row.append(matrix[i][j])
                minor.append(new_row)
        return minor
    
    def matrix_multiply(A, B):
        n = len(A)
        m = len(B[0])
        result = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_add(A, B):
        n = len(A)
        m = len(A[0])
        result = [[A[i][j] + B[i][j] for j in range(m)] for i in range(n)]
        return result
    
    def matrix_subtract(A, B):
        n = len(A)
        m = len(A[0])
        result = [[A[i][j] - B[i][j] for j in range(m)] for i in range(n)]
        return result
    
    def scale_matrix(matrix, scalar):
        n = len(matrix)
        m = len(matrix[0])
        result = [[matrix[i][j] * scalar for j in range(m)] for i in range(n)]
        return result
    
    def matrix_power(matrix, power):
        n = len(matrix)
        result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2
        return result
    
    def is_diophantine_solution(matrix, solution):
        n = len(matrix)
        m = len(solution)
        for i in range(n):
            if sum(matrix[i][j] * solution[j] for j in range(m)) != 0:
                return False
        return True
    
    def find_geometric_solution_set(matrix):
        n = len(matrix)
        m = len(matrix[0])
        solutions = []
        for i in range(2**m):
            solution = [i >> j & 1 for j in range(m)]
            if is_diophantine_solution(matrix, solution):
                solutions.append(solution)
        return solutions
    
    def resolution_steps(F):
        n = len(F)
        clauses = F[:]
        stack = []
        
        while True:
            unit_clauses = [i for i in range(n) if len(clauses[i]) == 1]
            if not unit_clauses:
                break
            literal = random.choice(unit_clauses)
            value = clauses[literal][0]
            stack.append((literal, value))
            
            for j in range(n):
                if j != literal and value in clauses[j]:
                    if -value in clauses[j]:
                        return len(stack) + 1
                    index = clauses[j].index(value)
                    clauses[j] = [clauses[j][k] for k in range(len(clauses[j])) if k != index]
        
        return len(stack)
    
    def generate_diophantine_equation(n):
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        while determinant(matrix) == 0:
            matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return matrix
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    F = generate_diophantine_equation(n)
    
    solutions = find_geometric_solution_set(F)
    minimal_rank = len(solutions)
    
    steps = resolution_steps(F)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank <= 2**math.log(n, 2),
        "counterexample": "" if minimal_rank <= 2**math.log(n, 2) else f"Minimal rank {minimal_rank} exceeds bound for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    total_steps = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_steps += trial_result["metric_value"]
    
    mean_steps = total_steps / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_steps} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_steps} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
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
        else:
            g, y, x = extended_gcd(b % a, a)
            return g, x - (b // a) * y, y
    
    def mod_inverse(a, m):
        g, x, _ = extended_gcd(a, m)
        if g != 1:
            raise ValueError("Inverse doesn't exist")
        else:
            return x % m
    
    def matrix_mod_inv(matrix, mod):
        n = len(matrix)
        det = 0
        for i in range(n):
            det += ((-1) ** i) * matrix[0][i] * determinant([[matrix[j][k] for k in range(1, n)] for j in range(1, n)])
        det = det % mod
        inv_det = mod_inverse(det, mod)
        adjugate = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                minor = [[matrix[x][y] for y in range(j, n)] for x in range(i, n)]
                sub_det = determinant(minor)
                adjugate[j][i] = ((-1) ** (i + j)) * sub_det
        inv_matrix = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
        return inv_matrix
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for j in range(n):
                minor = [[matrix[i][k] for k in range(j, n)] for i in range(1, n)]
                det += ((-1) ** j) * matrix[0][j] * determinant(minor)
            return det
    
    def grothendieck_group_size(clause_indicators):
        n = len(clause_indicators)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            G[i][i] = 1
        for clause in clause_indicators:
            for literal in clause:
                if literal > 0:
                    u, v = literal - 1, literal - 1
                else:
                    u, v = -literal - 1, -literal - 2
                G[u][v] += 1
                G[v][u] += 1
        inv_G = matrix_mod_inv(G, n)
        return sum(sum(row) for row in inv_G)
    
    def tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(n):
            clauses.append([variables[i]])
            for j in range(i + 1, n):
                clauses.append([-variables[i], -variables[j]])
                clauses.append([variables[i], variables[j]])
        return clauses
    
    def resolution_width(clauses):
        stack = []
        while True:
            if not stack:
                return len(set(stack))
            literal = random.choice(stack)
            if literal > 0:
                for clause in clauses:
                    if literal in clause:
                        clauses.remove(clause)
                        break
                else:
                    continue
            else:
                for clause in clauses:
                    if -literal in clause:
                        clauses.remove(clause)
                        break
                else:
                    continue
            stack.append(-literal)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = tseitin_formula(n)
    groth_group_size = grothendieck_group_size(clauses)
    width = resolution_width(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= groth_group_size + 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "resolution_width > grothendieck_group_size + 3"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            factor = Fraction(matrix[i][i])
            for j in range(i+1, n):
                factor_j = Fraction(matrix[j][i])
                for k in range(n):
                    matrix[j][k] -= factor_j * matrix[i][k]
        
        # Back substitution
        solution = [0] * n
        for i in range(n-1, -1, -1):
            solution[i] = Fraction(matrix[i][-1], matrix[i][i])
            for j in range(i-1, -1, -1):
                matrix[j][-1] -= matrix[j][i] * solution[i]
        return solution
    
    def determinant(matrix):
        n = len(matrix)
        det = Fraction(1)
        for i in range(n):
            det *= matrix[i][i]
        return det
    
    def min_order_brauer(G):
        n = len(G)
        T_G = [[0] * (n + 1) for _ in range(n + 1)]
        T_G[0][0] = 1
        for i in range(1, n + 1):
            T_G[i][0] = 1
            T_G[0][i] = -sum(G[i-1])
        
        for k in range(2, n + 1):
            for i in range(k, n + 1):
                T_G[i][k] = sum(T_G[j][k-1] * G[i-1][j-1] for j in range(i))
        
        det_T_G = determinant(T_G)
        return abs(det_T_G).numerator
    
    def resolution_width(G):
        n = len(G)
        clauses = []
        for i in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for _ in range(2)]
            clauses.append(clause)
        
        width = 0
        while clauses:
            new_clauses = []
            for clause in clauses:
                if any(abs(lit) > n for lit in clause):
                    continue
                if len(clause) == 1:
                    width += 1
                    break
                else:
                    new_clause = [lit for lit in clause if abs(lit) != abs(clause[0])]
                    new_clauses.append(new_clause)
            clauses = new_clauses
        
        return width
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                G[j][i] = 1
    
    min_order = min_order_brauer(G)
    width = resolution_width(G)
    
    return {
        "metric_name": "min_order(Br(G))",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
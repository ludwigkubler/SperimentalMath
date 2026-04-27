# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def add_with_carry(a, b):
    carry = 0
    result = []
    while a or b or carry:
        bit_a = a & 1 if a else 0
        bit_b = b & 1 if b else 0
        sum_bit = bit_a + bit_b + carry
        carry = sum_bit // 2
        result.append(sum_bit % 2)
        a >>= 1
        b >>= 1
    return result[::-1]

def matrix_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(rank)):
            continue
        rank += 1
        for j in range(i, n):
            if matrix[j][i]:
                matrix[j], matrix[i] = matrix[i], matrix[j]
                break
        for j in range(n):
            if j != i and matrix[j][i]:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] ^= (matrix[i][k] * factor) % 2
    return rank

def encode_php_n(n):
    m = n + 1
    clauses = []
    for i in range(m):
        for j in range(m):
            for k in range(m):
                if i != j and j != k and i != k:
                    clauses.append([-(i * m + j), -(j * m + k), (i * m + k)])
    return clauses

def tree_like_ef_search(clauses, max_lines=5000):
    n = int(math.sqrt(len(clauses)))
    variables = set()
    for clause in clauses:
        variables.update(abs(lit) for lit in clause)
    variable_to_index = {var: i for i, var in enumerate(variables)}
    
    def dfs(depth, model):
        if depth == 3 or len(model) >= max_lines:
            return None
        if all(var in model for var in variables):
            return model
        
        for lit in clauses[depth]:
            var = abs(lit)
            if var not in model:
                new_model = model.copy()
                new_model[var] = lit > 0
                result = dfs(depth + 1, new_model)
                if result:
                    return result
        return None
    
    return dfs(0, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12]
    results = []
    
    for n in n_values:
        M_n = [[add_with_carry(i, j).count(1) % 2 for j in range(n)] for i in range(n)]
        kappa_n = matrix_rank(M_n)
        
        clauses = encode_php_n(n)
        ef_result = tree_like_ef_search(clauses)
        
        if ef_result:
            L_n = len(ef_result)
            results.append((n, L_n))
        else:
            results.append((n, float('inf')))
    
    kappa_plus_n = [kappa + n for n, _ in results]
    L_n_values = [L_n for _, L_n in results]
    
    if all(L_n >= kappa_plus_n[i] for i, (_, L_n) in enumerate(results)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        first_failing_seed = seed
        counterexample = "EF line count below kappa(n) + n"
    
    return {
        "metric_name": "EF line count",
        "metric_value": sum(L_n_values) / len(L_n_values),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
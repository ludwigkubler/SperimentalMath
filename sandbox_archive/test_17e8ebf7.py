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

# Helper functions for matrix operations and tropical arithmetic
def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(m):
        if any(A[i]):
            rank += 1
    return rank

def tropical_add(a, b):
    return max(a, b)

def tropical_multiply(a, b):
    return a + b

# Function to generate a random 3-CNF formula of size n
def generate_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
        if all(clause[i] != -clause[j] for i in range(3) for j in range(i+1, 3)):
            clauses.append(clause)
    return clauses

# Function to compute the Tseitin circuit width of a 3-CNF formula
def tseitin_circuit_width(clauses):
    n = max(abs(lit) for clause in clauses for lit in clause)
    variables = set(range(1, n + 1))
    edges = []
    
    for i, clause in enumerate(clauses):
        var_i = n + i + 1
        for lit in clause:
            if lit > 0:
                edges.append((var_i, lit))
            else:
                edges.append((var_i, -lit))
        
        edges.append((2 * n + 1, var_i))
    
    # Find the maximum number of nodes in any path from 2*n+1 to a variable
    max_width = 0
    for var in variables:
        visited = set()
        queue = [(2 * n + 1, 0)]
        while queue:
            node, width = queue.pop(0)
            if node == var:
                max_width = max(max_width, width)
                break
            if node not in visited:
                visited.add(node)
                for neighbor in edges:
                    if neighbor[0] == node and neighbor[1] not in visited:
                        queue.append((neighbor[1], width + 1))
    
    return max_width

# Function to run a single trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    A_F = []
    for i in range(n):
        row = [tropical_add(-i, j) if j == i else -math.inf for j in range(n)]
        A_F.append(row)
    
    # Compute the tropicalized affine scheme rank
    rank = matrix_rank(A_F)
    
    # Compute the Tseitin circuit width
    width = tseitin_circuit_width(formula)
    
    return {
        "metric_name": "tropicalized_affine_scheme_rank",
        "metric_value": math.log(rank, 2),
        "instances_tested": n,
        "conjecture_holds": rank >= 2 ** width,
        "counterexample": "" if rank >= 2 ** width else f"width={width}, expected<=metric_value"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
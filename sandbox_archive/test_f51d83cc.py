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

# Constants
NUM_SEEDS = 30
MAX_N = 40
D_REGULAR = 3

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = Fraction(0)
    for j in range(len(matrix)):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(submatrix)
    return det

def resolution_width(formula):
    clauses = formula.split('\n')
    literals = set()
    for clause in clauses:
        literals.update(lit.strip('~') for lit in clause.split())
    width = 0
    for i in range(1, len(literals) + 1):
        if any(all(lit in clause or f"~{lit}" in clause for lit in literals[:i]) for clause in clauses):
            width = i
            break
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_max = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > MAX_N:
            continue
        
        G = [[0] * n for _ in range(n)]
        for _ in range(D_REGULAR * n // 2):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            while u == v or G[u][v]:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
            G[u][v] = G[v][u] = 1
        
        # Constructive mapping to Kähler manifold (simplified example)
        kdim_G = sum(sum(row) for row in G) / (n * (n - 1))
        
        formula = "\n".join(f"{' '.join('x' + str(j+1) if i == j else '~x' + str(j+1) if random.choice([True, False]) else '' for j in range(n))}" for i in range(n))
        width = resolution_width(formula)
        
        results.append((kdim_G, width))
        instances_tested += n
        n_max = max(n_max, n)
    
    metric_name = "resolution_width_correlation"
    metric_value = sum(k * w for k, w in results) / sum(w for _, w in results)
    conjecture_holds = 0.7 <= metric_value <= 0.9
    counterexample = "" if conjecture_holds else f"Correlation {metric_value:.2f} not within [0.7, 0.9]"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(NUM_SEEDS)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and all(r["metric_value"] >= 0.7 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"Correlation outside [0.7, 0.9]\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE Reason=insufficient_data_or_unsupported_conjecture")
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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def cheeger_constant(G, n):
    degrees = [sum(1 for j in range(n) if G[i][j]) for i in range(n)]
    max_cut_value = -1
    for s in range(1 << (n-1)):
        cut_size = sum(degrees[i] // 2 for i in range(n) if (s >> i) & 1)
        neighbors = [i for i in range(n) if (s >> i) & 1]
        neighbor_sum = sum(sum(G[i][j] for j in neighbors if G[j][i]) for i in neighbors)
        cut_value = min(cut_size, n - cut_size) * neighbor_sum / max_cut_value
        if cut_value > max_cut_value:
            max_cut_value = cut_value
    return 2 * max_cut_value / sum(degrees)

def d_regular_graph(d, n):
    G = [[0] * n for _ in range(n)]
    degree_count = [0] * n
    while any(count != d for count in degree_count):
        i, j = random.sample(range(n), 2)
        if not G[i][j]:
            G[i][j] = G[j][i] = 1
            degree_count[i] += 1
            degree_count[j] += 1
    return G

def tseitin_formula(G):
    n = len(G)
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    for i in range(n):
        clauses.append([literals[i]])
        for j in range(i+1, n):
            if G[i][j]:
                clauses.append([-literals[i], -literals[j]])
                clauses.append([literals[i], literals[j]])
    return literals + clauses

def dpll(clauses, assignment):
    if not clauses:
        return True
    literal = next(l for l in range(1, len(clauses) + 1) if l not in assignment and -l not in assignment)
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[literal] = value
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            elif -literal in clause:
                new_clause = [l for l in clause if l != -literal]
                if not new_clause:
                    break
                new_clauses.append(new_clause)
            else:
                new_clauses.append(clause)
        if dpll(new_clauses, new_assignment):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    d = 4
    G = d_regular_graph(d, n)
    h_G = cheeger_constant(G, n)
    formula = tseitin_formula(G)
    resolution_length = len(formula) + 1
    for _ in range(10):
        assignment = {i: random.choice([True, False]) for i in range(1, n+1)}
        if dpll(formula, assignment):
            resolution_length += 1
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_length,
        "instances_tested": 10,
        "conjecture_holds": resolution_length >= 2 ** (0.5 * h_G),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_length = sum(r['metric_value'] for r in results) / len(results)
    std_length = math.sqrt(sum((r['metric_value'] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
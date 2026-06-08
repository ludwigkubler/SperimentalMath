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

def generate_boolean_formula(n):
    if n == 1:
        return random.choice(['0', '1'])
    else:
        op = random.choice(['&', '|'])
        left = generate_boolean_formula(n // 2)
        right = generate_boolean_formula(n - n // 2)
        return f'({left} {op} {right})'

def evaluate_formula(formula):
    if formula == '0':
        return False
    elif formula == '1':
        return True
    else:
        op, left, right = formula[1], eval(formula[2:-1]), eval(formula[-2])
        if op == '&':
            return left and right
        elif op == '|':
            return left or right

def compute_simplicial_complex(phi):
    n = phi.count('(')
    simplicial_complex = []
    for i in range(1, 2**n):
        binary = format(i, f'0{n}b')
        assignment = {chr(ord('a') + j): int(binary[j]) for j in range(n)}
        if evaluate_formula(phi, assignment):
            simplicial_complex.append([assignment[chr(ord('a') + j)] for j in range(n)])
    return simplicial_complex

def compute_local_coherence(simplicial_complex):
    n = len(simplicial_complex)
    if n == 0:
        return 0
    max_dimension = max(len(face) for face in simplicial_complex)
    boundary_matrix = [[0] * (2**n - 1) for _ in range(max_dimension + 1)]
    for face in simplicial_complex:
        dimension = len(face)
        for i in range(2**n):
            binary = format(i, f'0{n}b')
            if all(binary[j] == '1' for j in face):
                boundary_matrix[dimension][i] += 1
    kernel = []
    for col in range(2**n - 1):
        pivot_row = None
        for row in range(max_dimension + 1):
            if boundary_matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is not None:
            for i in range(col, 2**n - 1):
                boundary_matrix[pivot_row][i], boundary_matrix[col][i] = boundary_matrix[col][i], boundary_matrix[pivot_row][i]
            for row in range(max_dimension + 1):
                if row != pivot_row and boundary_matrix[row][col] != 0:
                    factor = Fraction(boundary_matrix[row][col], boundary_matrix[pivot_row][col])
                    for i in range(col, 2**n - 1):
                        boundary_matrix[row][i] -= factor * boundary_matrix[pivot_row][i]
        else:
            kernel.append([boundary_matrix[row][col] for row in range(max_dimension + 1)])
    return len(kernel)

def compute_frege_proof_depth(phi):
    stack = []
    depth = 0
    max_depth = 0
    i = 0
    while i < len(phi):
        if phi[i] == '(':
            stack.append('(')
            i += 1
        elif phi[i] == ')':
            stack.pop()
            i += 1
        else:
            i += 1
        depth = len(stack)
        max_depth = max(max_depth, depth)
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        phi = generate_boolean_formula(n)
        simplicial_complex = compute_simplicial_complex(phi)
        local_coherence = compute_local_coherence(simplicial_complex)
        proof_depth = compute_frege_proof_depth(phi)
        results.append({
            "n": n,
            "phi": phi,
            "local_coherence": local_coherence,
            "proof_depth": proof_depth
        })
    correlation = 0
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            r1 = results[i]
            r2 = results[j]
            if r1["n"] == r2["n"]:
                correlation += (r1["local_coherence"] - r2["local_coherence"]) * (r1["proof_depth"] - r2["proof_depth"])
    correlation /= len(results) ** 2
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) > 0.7) / len(results)
    if all(abs(r["metric_value"]) > 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if abs(r["metric_value"]) < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
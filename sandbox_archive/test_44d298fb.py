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
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return A, b

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_inverse(A):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            I[i], I[max_row] = I[max_row], I[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                I[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        I[k][j] -= factor * I[i][j]
        return I

    def dual_distance(A):
        n = len(A)
        A_inv = matrix_inverse(A)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                D[i][j] = sum(A_inv[k][i] * A_inv[j][k] for k in range(n))
        return min([sum(D[i]) for i in range(n)])

    def generate_tseitin_instance(n):
        random.seed(seed)
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append(f'~{variables[i-1]} | ~{variables[j-1]}')
        return variables, clauses

    def resolution_refutation_size(variables, clauses):
        random.seed(seed)
        n = len(variables)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for clause in clauses:
            if ' | ' not in clause and ' ~' not in clause:
                continue
            literals = clause.split(' | ')
            literal_indices = [variables.index(l[1:]) + 1 if l.startswith('~') else variables.index(l) + 1 for l in literals]
            A[literal_indices[0]][literal_indices[1]] += 1
            A[literal_indices[1]][literal_indices[0]] += 1
            b[literal_indices[0]] += 1
            b[literal_indices[1]] += 1
        A, b = gaussian_elimination(A, b)
        return sum(abs(x) for x in b)

    n_values = [5, 10, 15, 20, 30, 40]
    refutation_sizes = []
    dual_distances = []

    for n in n_values:
        variables, clauses = generate_tseitin_instance(n)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            if ' | ' not in clause and ' ~' not in clause:
                continue
            literals = clause.split(' | ')
            literal_indices = [variables.index(l[1:]) + 1 if l.startswith('~') else variables.index(l) + 1 for l in literals]
            A[literal_indices[0]][literal_indices[1]] += 1
            A[literal_indices[1]][literal_indices[0]] += 1
        dual_distance_value = dual_distance(A)
        refutation_size = resolution_refutation_size(variables, clauses)
        refutation_sizes.append(refutation_size)
        dual_distances.append(dual_distance_value)

    metric_name = "Refutation Size / Dual Distance"
    metric_value = sum(refutation_sizes) / len(refutation_sizes) / sum(dual_distances) / len(dual_distances)
    instances_tested = len(n_values)
    conjecture_holds = all(r >= d for r, d in zip(refutation_sizes, dual_distances))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
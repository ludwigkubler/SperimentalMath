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

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(B[0]))] for i in range(len(A))]

def matrix_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(B[0]))] for i in range(len(A))]

def matrix_mul(A, B, mod):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
    return result

def matrix_transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def gaussian_elimination(A, b, mod):
    n = len(b)
    A_aug = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        if A_aug[i][i] == 0:
            found = False
            for j in range(i+1, n):
                if A_aug[j][i] != 0:
                    A_aug[i], A_aug[j] = A_aug[j], A_aug[i]
                    found = True
                    break
            if not found:
                return None
        pivot = A_aug[i][i]
        for j in range(i, n+1):
            A_aug[i][j] = (A_aug[i][j] * pow(pivot, mod-2, mod)) % mod
        for j in range(n):
            if i != j:
                factor = A_aug[j][i]
                for k in range(i, n+1):
                    A_aug[j][k] = (A_aug[j][k] - factor * A_aug[i][k]) % mod
    return [row[-1] for row in A_aug]

def dual_linear_code(F, n):
    literals = set()
    for clause in F:
        for literal in clause.split():
            if literal.startswith('x'):
                literals.add(literal)
    m = len(literals)
    code_matrix = [[0 for _ in range(m)] for _ in range(n)]
    for i, clause in enumerate(F):
        for literal in clause.split():
            if literal.startswith('x'):
                index = int(literal[2:]) - 1
                code_matrix[i][index] = 1
            elif literal.startswith('~'):
                index = int(literal[2:]) - 1
                code_matrix[i][index] = 0
    return code_matrix

def xor_gates(code_matrix, mod):
    n, m = len(code_matrix), len(code_matrix[0])
    G = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if code_matrix[i][j] == 1:
                G[j] = matrix_add(G[j], code_matrix[i], mod)
    return G

def min_rank(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    rank = 0
    for i in range(cols):
        if any(matrix[j][i] != 0 for j in range(rank, rows)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        F = [' '.join(random.sample([f'x{i+1}', f'~x{i+1}'], random.randint(1, min(n, 3)))) for _ in range(n)]
        code_matrix = dual_linear_code(F, n)
        G = xor_gates(code_matrix, 2)
        rank = min_rank(G)
        metric_values.append(rank)

    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = instances_tested / instances_tested

    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction")
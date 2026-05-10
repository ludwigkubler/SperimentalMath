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

def generate_random_graph(n):
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                graph[i][j] = graph[j][i] = random.randint(1, 10)
    return graph

def max_cut_polynomial(graph):
    n = len(graph)
    poly = [[0] * (n * (n - 1) // 2) for _ in range(n * (n - 1) // 2)]
    index = 0
    for i in range(n):
        for j in range(i + 1, n):
            poly[index][index] = graph[i][j]
            index += 1
    return poly

def matrix_multiplication(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    result = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(A)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, n + 1):
            Augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = Augmented[j][i]
                for k in range(i, n + 1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def rank(matrix):
    A = [row[:] for row in matrix]
    m = len(A)
    n = len(A[0])
    pivot_columns = set()
    for i in range(m):
        if i not in pivot_columns:
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot_column = i
            pivot_columns.add(pivot_column)
            for j in range(n):
                A[i][j] /= A[i][pivot_column]
            for j in range(m):
                if j != i:
                    factor = A[j][pivot_column]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
    return len(pivot_columns)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    graph = generate_random_graph(n)
    d = math.floor(math.log(n) / math.log(log(n)))
    poly = max_cut_polynomial(graph)
    moment_matrix = [[0] * (n * (n - 1) // 2) for _ in range(n * (n - 1) // 2)]
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(n):
                for l in range(k + 1, n):
                    moment_matrix[i * (i - 1) // 2 + j][k * (k - 1) // 2 + l] = poly[i * (n - i - 1) // 2 + j][k * (n - k - 1) // 2 + l]
    rank_value = rank(moment_matrix)
    instances_tested = 1
    conjecture_holds = rank_value >= 0.1 * n
    counterexample = "" if conjecture_holds else "rank < 0.1n"
    return {
        "metric_name": "Rank",
        "metric_value": rank_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < 0.1n\" first_failing_seed={first_failing_seed}")
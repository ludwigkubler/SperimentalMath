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

def generate_random_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        clauses.append(clause)
    return clauses

def communication_matrix(clauses, n):
    m = 2 ** n
    matrix = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            x = [i >> (n - k) & 1 for k in range(n)]
            y = [j >> (n - k) & 1 for k in range(n)]
            if all(x[var - 1] == y[var - 1] or var not in clause for clause in clauses):
                matrix[i][j] = 1
    return matrix

def viterbi_algorithm(matrix, n):
    m = 2 ** n
    dist = [[math.inf] * m for _ in range(m)]
    prev = [[None] * m for _ in range(m)]
    dist[0][0] = 0
    
    for k in range(1, m):
        for i in range(m):
            for j in range(m):
                if matrix[i][j] == 1:
                    d = dist[i][k - 1] + abs(i ^ j)
                    if d < dist[j][k]:
                        dist[j][k] = d
                        prev[j][k] = i
    
    return dist, prev

def backtrack(prev, n):
    m = 2 ** n
    path = []
    current = m - 1
    for k in range(m - 1, 0, -1):
        path.append(current)
        current = prev[current][k]
    path.append(0)
    return path[::-1]

def persistent_homology(matrix, n):
    dist, _ = viterbi_algorithm(matrix, n)
    barcode_lengths = []
    for i in range(n + 1):
        max_length = 0
        for j in range(2 ** n):
            if dist[j][j] == i:
                path = backtrack(prev, n)
                length = len(path) - 1
                if length > max_length:
                    max_length = length
        barcode_lengths.append(max_length)
    return barcode_lengths

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    clauses = generate_random_3cnf(n)
    matrix = communication_matrix(clauses, n)
    barcode_lengths = persistent_homology(matrix, n)
    sum_barcode_lengths = sum(barcode_lengths)
    
    # Karchmer-Wigderson protocol cost for 3-CNF is Θ(n log n)
    cc_f = n * math.log2(n)
    
    metric_value = sum_barcode_lengths / (cc_f * math.log(2))
    instances_tested = 1
    conjecture_holds = abs(metric_value - 1) < 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Sum of Barcode Lengths / log CC(f)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
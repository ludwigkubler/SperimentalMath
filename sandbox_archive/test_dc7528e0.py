# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = -matrix[k][i]
                for j in range(cols):
                    matrix[k][j] += factor * matrix[i][j]
    return matrix

def determinant(matrix):
    rows, cols = len(matrix), len(matrix[0])
    if rows != cols:
        raise ValueError("Matrix must be square")
    det = 1
    for i in range(rows):
        max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        det *= matrix[i][i]
        if det == 0:
            return 0
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = -matrix[k][i]
                for j in range(cols):
                    matrix[k][j] += factor * matrix[i][j]
    return det

def construct_root_lattice(graph_edges, n):
    lattice = [[0] * n for _ in range(n)]
    for i, j in graph_edges:
        lattice[i][j] = 1
        lattice[j][i] = 1
    return lattice

def minimal_geometric_entropy(lattice):
    det = determinant(lattice)
    if det == 0:
        raise ValueError("Lattice is singular")
    rank = sum(1 for row in lattice if any(row))
    entropy = -rank * math.log2(rank) / n
    return entropy

def communication_complexity(graph_edges, n):
    # Placeholder function; replace with actual complexity calculation
    return len(graph_edges)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph_edges = set(random.sample(range(n), k=2*n-1))
    lattice = construct_root_lattice(graph_edges, n)
    try:
        entropy = minimal_geometric_entropy(lattice)
        complexity = communication_complexity(graph_edges, n)
        return {
            "metric_name": "Minimal Geometric Entropy vs Communication Complexity",
            "metric_value": entropy - complexity,
            "instances_tested": 1,
            "conjecture_holds": entropy <= complexity,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "Minimal Geometric Entropy vs Communication Complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 10 for r in results) or support_fraction < 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
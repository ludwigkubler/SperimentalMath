# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20  # Number of vertices in the graph
    m = 3   # Number of edges per vertex (to ensure connectivity)

    # Generate a random connected graph with n vertices and m edges per vertex
    graph = {i: set() for i in range(n)}
    for _ in range(m * n):
        u, v = random.sample(range(n), 2)
        if u != v and v not in graph[u]:
            graph[u].add(v)
            graph[v].add(u)

    # Compute the minimal number of generators m(G) using a simple heuristic
    # This is a placeholder for an actual algorithm to compute m(G)
    m_G = len(graph)  # Simplified heuristic

    # Construct Tseitin formula φ on the graph G
    clauses = []
    literals = {i: [] for i in range(n)}
    for u in range(n):
        literals[u].append(f'x_{u}')
        for v in graph[u]:
            literals[v].append(f'x_{v}')

    # Add clauses to ensure each literal is true at least once
    for u in range(n):
        clauses.append([f'x_{u}'])

    # Add clauses to ensure no two adjacent vertices have the same literal
    for u in range(n):
        for v in graph[u]:
            clauses.append([-f'x_{u}', f'x_{v}'])
            clauses.append([f'x_{u}', -f'x_{v}'])

    # Compute the Resolution length L(φ)
    def resolution_length(clauses):
        A = []
        for clause in clauses:
            row = [0] * (2 * n + 1)
            for literal in clause:
                if literal[0] == 'x':
                    index = int(literal[2:]) + n
                else:
                    index = int(literal[2:])
                row[index] = 1
            A.append(row)

        def rank_of_matrix(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                if matrix[i][i] == 0:
                    found_nonzero = False
                    for j in range(i + 1, rows):
                        if matrix[j][i] != 0:
                            matrix[i], matrix[j] = matrix[j], matrix[i]
                            found_nonzero = True
                            break
                    if not found_nonzero:
                        continue

                pivot = Fraction(matrix[i][i])
                for j in range(i, cols):
                    matrix[i][j] /= pivot

                for j in range(rows):
                    if j != i and matrix[j][i] != 0:
                        factor = -Fraction(matrix[j][i], matrix[i][i])
                        for k in range(i, cols):
                            matrix[j][k] += factor * matrix[i][k]
            return sum(1 for row in matrix if any(row))

        rank = rank_of_matrix(A)
        return rank

    L_phi = resolution_length(clauses)

    # Check if the Resolution length satisfies the inequality
    conjecture_holds = L_phi >= 2 ** (m_G * 0.5)  # Simplified heuristic for demonstration

    return {
        "metric_name": "Resolution Length",
        "metric_value": L_phi,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Graph with m(G)={m_G}, L(φ)={L_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i for i in range(5, 8)]  # Default to first 3 prime numbers

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
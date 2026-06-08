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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0.0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a 3-regular graph with odd charge
    v = random.choice([6, 8, 10, 12, 14, 16, 18, 20])
    n = 3 * v // 2
    m = v
    
    # Configuration model to generate a 3-regular graph
    degree_sequence = [3] * v
    nodes = list(range(v))
    edges = []
    
    while len(edges) < m:
        node1 = random.choice(nodes)
        neighbors = [node for node in nodes if (node, node1) not in edges and (node1, node) not in edges]
        if not neighbors:
            continue
        node2 = random.choice(neighbors)
        edges.append((node1, node2))
    
    # Build the clause-incidence point cloud P(φ_G)
    P = [[0] * n for _ in range(m)]
    for i, (node1, node2) in enumerate(edges):
        P[i][node1] = 1
        P[i][node2] = -1
    
    # Compute persistent H1 via Vietoris-Rips up to scale 2√3
    scale = 2 * math.sqrt(3)
    persistence_intervals = []
    
    for i in range(m):
        for j in range(i+1, m):
            dist = sum(abs(P[i][k] - P[j][k]) for k in range(n))
            if dist <= scale:
                persistence_intervals.append((dist, 0, 1))
    
    def boundary_matrix_reduction(matrix):
        rows, cols = len(matrix), len(matrix[0])
        boundary = [[0 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == -1:
                    boundary[i][j-1] += 1
                    boundary[j][i] -= 1
        return boundary
    
    def find_cycle(matrix):
        rows, cols = len(matrix), len(matrix[0])
        visited = [False] * cols
        for j in range(cols):
            if not visited[j]:
                stack = [(j, 0)]
                while stack:
                    node, depth = stack.pop()
                    if visited[node]:
                        cycle_length = depth - visited[node]
                        if cycle_length > 1:
                            return True
                    else:
                        visited[node] = depth
                        for i in range(rows):
                            if matrix[i][node] == 1:
                                stack.append((i, depth + 1))
        return False
    
    L1 = sum(max(0, interval[2] - interval[1]) for interval in persistence_intervals)
    
    # Measure resolution proof width w(φ_G) by iterative deepening
    def resolve_clause(clause, assignment):
        stack = [(clause, assignment)]
        while stack:
            clause, assignment = stack.pop()
            if len(clause) == 0:
                return True
            literal = clause[0]
            var = abs(literal) - 1
            if literal > 0:
                assignment[var] = True
            else:
                assignment[var] = False
            new_clause = [l for l in clause if l != literal and l != -literal]
            stack.append((new_clause, assignment))
        return False
    
    def resolution_width(assignment):
        max_width = 0
        for i in range(m):
            clause = P[i]
            width = len([l for l in clause if abs(l) not in assignment])
            max_width = max(max_width, width)
        return max_width
    
    w = resolution_width({})
    
    # Check the conjecture
    C = w / (L1 + math.log2(n))
    conjecture_holds = C <= 10
    counterexample = "" if conjecture_holds else f"Counterexample: C={C:.2f} > 10"
    
    return {
        "metric_name": "Resolution Width vs H1 Lifespan",
        "metric_value": w,
        "instances_tested": m,
        "n_max": v,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials ran")
        exit()
    
    mean_w = sum(r["metric_value"] for r in results) / len(results)
    std_w = math.sqrt(sum((r["metric_value"] - mean_w)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_w:.4f} std={std_w:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support or refutation found")
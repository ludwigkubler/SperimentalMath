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

def generate_projective_plane(q):
    if q < 2:
        raise ValueError("q must be at least 2")
    
    points = list(range(q**2 + q + 1))
    lines = []
    
    for i in range(q**2 + q + 1):
        line = [i]
        for j in range(1, q + 1):
            line.append((i * j) % (q**2 + q + 1))
        lines.append(line)
    
    return points, lines

def adjacency_matrix(points, lines):
    n = len(points)
    adj_matrix = [[0] * n for _ in range(n)]
    
    for point in points:
        for line in lines:
            if point in line:
                for other_point in line:
                    if other_point != point:
                        adj_matrix[points.index(point)][points.index(other_point)] = 1
    
    return adj_matrix

def is_connected(matrix):
    n = len(matrix)
    visited = [False] * n
    stack = [0]
    
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in range(n):
                if matrix[node][neighbor] == 1 and not visited[neighbor]:
                    stack.append(neighbor)
    
    return all(visited)

def min_width_abp(adj_matrix):
    n = len(adj_matrix)
    dp = [[float('inf')] * (n + 1) for _ in range(n)]
    dp[0][1] = 0
    
    for k in range(2, n + 1):
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1:
                    dp[j][k] = min(dp[j][k], dp[i][k - 1] + 1)
    
    return dp[n - 1][n]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        q = 2 ** (n // (n + 1))
        points, lines = generate_projective_plane(q)
        
        if not is_connected(adjacency_matrix(points, lines)):
            return {
                "metric_name": "ABP Width",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        width = min_width_abp(adjacency_matrix(points, lines))
        results.append(width)
    
    mean = sum(results) / len(results)
    conjecture_holds = all(w >= q**2 + q + 1 for w in results)
    counterexample = "" if conjecture_holds else f"q={q}, expected {q**2+q+1}, got {min(results)}"
    
    return {
        "metric_name": "ABP Width",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(1, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
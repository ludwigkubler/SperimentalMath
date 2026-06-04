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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique_free_graph(n, k):
        if n < k + 1:
            return None
        G = [[0] * n for _ in range(n)]
        nodes = list(range(n))
        for i in range(k + 1):
            subset = random.sample(nodes, k)
            for u in subset:
                for v in subset:
                    if u != v:
                        G[u][v] = G[v][u] = 1
        return G
    
    def alexander_defect(G):
        n = len(G)
        if any(sum(row) % 2 == 0 for row in G):
            return 0
        A = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    A[i][j] = Fraction(-1)
                    A[j][i] = Fraction(-1)
        I = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            I[i][i] = Fraction(1)
        
        def gaussian_elimination(M, b):
            n = len(M)
            for i in range(n):
                max_row = i
                for j in range(i + 1, n):
                    if abs(M[j][i]) > abs(M[max_row][i]):
                        max_row = j
                M[i], M[max_row] = M[max_row], M[i]
                b[i], b[max_row] = b[max_row], b[i]
                
                factor = M[i][i]
                for j in range(i, n):
                    M[i][j] /= factor
                b[i] /= factor
                
                for j in range(n):
                    if j != i:
                        factor = M[j][i]
                        for k in range(i, n):
                            M[j][k] -= factor * M[i][k]
                        b[j] -= factor * b[i]
            
            x = [0] * n
            for i in range(n - 1, -1, -1):
                x[i] = b[i]
                for j in range(i + 1, n):
                    x[i] -= M[i][j] * x[j]
            return x
        
        def determinant(M):
            n = len(M)
            if n == 2:
                return M[0][0] * M[1][1] - M[0][1] * M[1][0]
            det = Fraction(0)
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in M[1:]]
                det += (-1) ** j * M[0][j] * determinant(submatrix)
            return det
        
        def rank(M):
            n = len(M)
            r = 0
            for i in range(n):
                if any(M[i][j] != 0 for j in range(r)):
                    r += 1
            return r
        
        return rank(A) - determinant(I)
    
    def communication_complexity(G):
        n = len(G)
        nodes = list(range(n))
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if G[i][j] == 1]
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in nodes:
                        if G[node][neighbor] == 1 and neighbor not in visited:
                            stack.append(neighbor)
        
        max_clique_size = 0
        for subset in itertools.combinations(nodes, k + 1):
            clique = list(subset)
            visited = set()
            dfs(clique[0], visited)
            if len(visited) == len(clique):
                max_clique_size = max(max_clique_size, len(clique))
        
        return n - max_clique_size
    
    def spearman_correlation(x, y):
        n = len(x)
        rank_x = [sorted(x).index(xi) for xi in x]
        rank_y = [sorted(y).index(yi) for yi in y]
        d = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        return 1 - (6 * d) / (n * (n**2 - 1))
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            G = generate_k_clique_free_graph(n, k)
            if G is None:
                continue
            instances_tested += 1
            
            defect = alexander_defect(G)
            rank = communication_complexity(G)
            
            metric_values.append((defect, rank))
    
    if len(metric_values) < 24:
        return {
            "metric_name": "Spearman's Rank Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    x, y = zip(*metric_values)
    rho = spearman_correlation(x, y)
    
    return {
        "metric_name": "Spearman's Rank Correlation",
        "metric_value": abs(rho),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(rho) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation < 0.7\" first_failing_seed={first_failing_seed}")
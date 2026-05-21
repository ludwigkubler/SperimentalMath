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
    random.seed(seed)
    
    def build_X_G(G):
        m = len(G)
        X_G = [[0] * (3 * m) for _ in range(3 * m)]
        edge_to_index = {}
        
        # Add edges as 1-simplices
        for i in range(m):
            u, v = G[i]
            edge_to_index[(u, v)] = i
            X_G[2 * i][i] = 1
            X_G[2 * i + 1][(m + i) % (3 * m)] = 1
        
        # Add triples as 2-simplices
        for i in range(m):
            u, v = G[i]
            for j in range(i + 1, m):
                w, x = G[j]
                if {u, v} & {w, x}:
                    k = (m * 2 + (i * (i + 1) // 2 + j)) % (3 * m)
                    X_G[k][i] = 1
                    X_G[k][(m + i) % (3 * m)] = 1
                    X_G[k][(2 * m + j) % (3 * m)] = 1
        
        return X_G
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            pivot = A[i][i]
            for j in range(i, n):
                A[i][j] /= pivot
            
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        
        return A
    
    def compute_lambda_up(X_G):
        m = len(X_G)
        I = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
        D = [[sum(row) for row in X_G], [sum(col) for col in zip(*X_G)], [sum(sum(row[i:i+3]) for row in X_G) for i in range(0, m, 3)]]
        
        L1 = [[D[2][i] - D[1][j] if (i // 3 == j // 3 and i % 3 != j % 3) else 0 for j in range(m)] for i in range(m)]
        L1_inv = gaussian_elimination([[L1[i][j] / D[2][i] if j == i else 0 for j in range(m)] for i in range(m)])
        
        return min([D[1][i] - sum(L1_inv[j][i] * D[2][j] for j in range(m)) for i in range(m) if L1_inv[i][i] != 0])
    
    def dpll(G, c):
        stack = []
        backtrack_count = 0
        while True:
            assignment = {v: None for v in set(u for u, v in G)}
            for v in sorted(assignment.keys()):
                if assignment[v] is None:
                    assignment[v] = c[v]
                    stack.append((v, assignment))
                    break
            else:
                return backtrack_count
            
            while True:
                v, assignment = stack.pop()
                assignment[v] = 1 - assignment[v]
                backtrack_count += 1
                
                if all(assignment[u] == assignment[v] for u, v in G):
                    return backtrack_count
    
    n_values = [8, 10, 12, 14, 16, 18, 20]
    total_backtracks = 0
    lambda_ups = []
    
    for n in n_values:
        for _ in range(30):
            V = list(range(n))
            G = random.sample(list(itertools.combinations(V, 2)), n)
            c = {v: random.choice([0, 1]) for v in V}
            if sum(c.values()) % 2 == 0:
                continue
            
            X_G = build_X_G(G)
            lambda_up = compute_lambda_up(X_G)
            backtrack_count = dpll(G, c)
            
            total_backtracks += backtrack_count
            lambda_ups.append(lambda_up)
    
    mean_backtrack_rate = total_backtracks / (len(n_values) * 30)
    min_ratio = min(math.log2(backtrack_count) / (lambda_up * math.sqrt(n)) for n, backtrack_count, lambda_up in zip(n_values * 30, [total_backtracks] * len(n_values), lambda_ups))
    
    if mean_backtrack_rate > 0.8 * min_ratio:
        return {
            "metric_name": "mean_backtrack_rate",
            "metric_value": mean_backtrack_rate,
            "instances_tested": len(n_values) * 30,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        counterexample = f"n={n}, backtrack_count={backtrack_count}, lambda_up={lambda_up}"
        return {
            "metric_name": "mean_backtrack_rate",
            "metric_value": mean_backtrack_rate,
            "instances_tested": len(n_values) * 30,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] and n >= 18 and math.log2(r["metric_value"]) < 0.8 * (0.05 * r["lambda_up"] * math.sqrt(n)) for n, r in zip(n_values * 30, results)):
        counterexample = next((r["counterexample"] for r in results if r["conjecture_holds"] and n >= 18 and math.log2(r["metric_value"]) < 0.8 * (0.05 * r["lambda_up"] * math.sqrt(n))), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next((r for r in results if r['conjecture_holds'] and n >= 18), None))]}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")
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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def vandermonde_matrix(x, n):
        m = len(x)
        V = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                V[i][j] = x[i] ** j
        return V

    def solve_linear_system(A, b):
        A = gaussian_elimination([row + [b[i]] for i, row in enumerate(A)])
        m, n = len(A), len(A[0])
        x = [0] * (n - 1)
        for i in range(m - 1, -1, -1):
            x[i] = A[i][-1]
            for j in range(i + 1, n - 1):
                x[i] -= A[i][j] * x[j]
        return x

    def random_3_regular_graph(v):
        edges = set()
        while len(edges) < v:
            u = random.randint(0, v - 1)
            v = random.randint(0, v - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)

    def tseitin_formula(G):
        n = len(G)
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
        for u, v in G:
            clauses.append([-u - 1, v + 1])
            clauses.append([-v - 1, u + 1])
        return clauses

    def persistent_homology(clauses, scale):
        n = len(clauses)
        points = [[-1 if i % 2 == 0 else 1 for _ in range(n)] for _ in range(2)]
        birth = [math.inf] * n
        death = [-math.inf] * n
        
        def distance(p1, p2):
            return sum(abs(a - b) for a, b in zip(p1, p2))
        
        for i in range(n):
            if birth[i] == math.inf:
                birth[i] = 0
                queue = [i]
                while queue:
                    u = queue.pop()
                    for v in range(n):
                        if distance(points[u], points[v]) <= scale and death[v] == -math.inf:
                            death[v] = birth[u] + scale
                            queue.append(v)
        
        H1_lifespan = sum(death[i] - birth[i] for i in range(n) if birth[i] < math.inf and death[i] > -math.inf)
        return H1_lifespan

    def resolution_width(clauses, max_width):
        n = len(clauses)
        stack = []
        path = []
        
        def extend_clause(c):
            nonlocal stack, path
            for literal in c:
                if literal not in stack and -literal not in stack:
                    stack.append(literal)
                    path.append((c, literal))
                    return True
            return False
        
        def backtrack():
            nonlocal stack, path
            while stack:
                c, lit = path.pop()
                stack.remove(lit)
                for i, cl in enumerate(clauses):
                    if -lit in cl and not extend_clause(cl):
                        del clauses[i]
                        break
        
        for _ in range(max_width):
            if not any(extend_clause(c) for c in clauses):
                backtrack()
        
        return len(stack)

    v = random.choice([6, 8, 10, 12, 14, 16, 18, 20])
    G = random_3_regular_graph(v)
    if sum(1 for u, v in G) % 2 != 1:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": v,
            "conjecture_holds": False,
            "counterexample": "odd_charge_not_met"
        }
    
    clauses = tseitin_formula(G)
    L1 = persistent_homology(clauses, 2 * math.sqrt(3))
    w = resolution_width(clauses, 6)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w,
        "instances_tested": 1,
        "n_max": v,
        "conjecture_holds": True if w <= 10 * (L1 + math.log2(v)) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_w = sum(r["metric_value"] for r in results) / len(results)
        std_w = math.sqrt(sum((r["metric_value"] - mean_w) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_w} std={std_w} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
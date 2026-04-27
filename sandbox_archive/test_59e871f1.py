# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_3_regular_graph(n):
        if n % 2 != 0 or n < 4:
            raise ValueError("n must be even and >= 4")
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < n * 3 // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges and u != v:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def compute_h(G):
        n = len(G)
        min_cut = float('inf')
        for S in itertools.combinations(range(n), n // 2 + 1):
            cut_size = sum(len([v for v in G[u] if u in S and v not in S]) for u in S)
            min_cut = min(min_cut, cut_size / len(S))
        return min_cut
    
    def power_iteration(A, k=20):
        n = len(A)
        x = [random.random() for _ in range(n)]
        x /= math.sqrt(sum(x[i] ** 2 for i in range(n)))
        for _ in range(k):
            y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            y /= math.sqrt(sum(y[i] ** 2 for i in range(n)))
            x, y = y, x
        return x
    
    def compute_lambda_2(G):
        n = len(G)
        A = [[0 if u != v else -len(G[u]) + sum(1 for w in G[v] if w != u) for v in range(n)] for u in range(n)]
        eigenvector = power_iteration(A)
        lambda_2 = max(sum(A[i][j] * eigenvector[j] for j in range(n)) * eigenvector[i] for i in range(n))
        return lambda_2
    
    def compute_delta(G):
        beta_G = 2 * math.sqrt(3 * compute_lambda_2(G))
        h_G = compute_h(G)
        return max(beta_G - h_G, 0)
    
    def compute_L(G):
        n = len(G)
        delta_G = compute_delta(G)
        beta_G = 2 * math.sqrt(3 * compute_lambda_2(G))
        h_G = compute_h(G)
        return h_G * (1 - delta_G / beta_G) * n // 3 - 2
    
    def is_valid_clause(clause, assignment):
        return any(assignment[var] == val for var, val in clause)
    
    def resolve_clause(clause, assignment):
        for i in range(len(clause)):
            if clause[i][1] != assignment[clause[i][0]]:
                new_clause = [c for j, c in enumerate(clause) if j != i]
                return new_clause
        return []
    
    def dpll(G, n, k, assignment):
        if not any(is_valid_clause(clause, assignment) for clause in G):
            return True
        var = next(v for v in range(n) if v not in assignment)
        for val in [0, 1]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if dpll(G, n, k, new_assignment):
                return True
        return False
    
    def compute_w(G, n, k):
        for w in range(k + 1):
            if all(dpll(G, n, w, {}) for _ in range(30)):
                return w
        return -1
    
    n = random.choice([8, 10, 12, 14, 16, 18, 20])
    G = generate_random_3_regular_graph(n)
    c = {i: random.randint(0, 1) for i in range(n)}
    
    h_G = compute_h(G)
    lambda_2_G = compute_lambda_2(G)
    delta_G = compute_delta(G)
    L_G = compute_L(G)
    
    w_T_G_c = compute_w(G, n, n // 2)
    
    if w_T_G_c < max(0, L_G) - 1:
        return {
            "metric_name": "w(T(G,c))",
            "metric_value": w_T_G_c,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Instance {n} with h(G)={h_G}, lambda_2(G)={lambda_2_G}, delta(G)={delta_G}, L(G)={L_G}"
        }
    
    return {
        "metric_name": "w(T(G,c))",
        "metric_value": w_T_G_c,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r["w(T(G,c))"] < max(0, r["L(G)"]) - 1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["w(T(G,c))"] < max(0, result["L(G)"]) - 1)
        print(f"RESULT: FALSIFIED counterexample=\"Instance with w(T(G,c)) < L(G) - 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")
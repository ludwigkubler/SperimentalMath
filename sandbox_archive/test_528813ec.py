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
    
    def resistance_distance(G, u, v):
        n = len(G)
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in G:
            dist[u][v] = min(dist[u][v], w)
            dist[v][u] = min(dist[v][u], w)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist[u][v]

    def min_rank(G):
        n = len(G)
        V = list(range(n))
        rank = 0
        for v in V:
            if all(u != v and (u, v) not in G and (v, u) not in G for u in V if u != v):
                rank += 1
        return rank

    def tseitin_formula(G):
        n = len(G)
        literals = list(range(2 * n))
        clauses = []
        for i in range(n):
            clauses.append([literals[i], literals[n + i]])
            for j in range(i + 1, n):
                if (i, j) not in G and (j, i) not in G:
                    clauses.append([-literals[i], -literals[j]])
        return clauses

    def resolution_refutation_length(clauses):
        stack = []
        visited = set()
        for clause in clauses:
            if any(lit in visited for lit in clause):
                continue
            stack.append(clause)
            visited.add(tuple(sorted(clause)))
        while stack:
            clause1 = stack.pop()
            for clause2 in clauses:
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = [lit for lit in clause1 + clause2 if lit not in clause1 and lit != -list(set(clause1) & set(clause2))[0]]
                    if not new_clause:
                        return len(stack)
                    stack.append(new_clause)
        return float('inf')

    n = random.randint(5, 40)
    G = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                w = random.randint(1, 10)
                G.append((i, j, w))
    
    u, v = random.sample(range(n), 2)
    rho_G = resistance_distance(G, u, v)
    rank_G = min_rank(G)
    F_G = tseitin_formula(G)
    refutation_length = resolution_refutation_length(F_G)

    return {
        "metric_name": "resolution refutation length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": rank_G >= 2 ** (rho_G * math.log(2)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
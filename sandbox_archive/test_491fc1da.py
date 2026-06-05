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
    
    def generate_graph(n):
        G = [[0] * n for _ in range(n)]
        degree = 2
        if n % degree != 0:
            return None, None
        for i in range(n // degree):
            for j in range(degree):
                u = i * degree + j
                v = (i + 1) % (n // degree) * degree + (j + 1) % degree
                G[u][v] = 1
                G[v][u] = 1
        return G, degree
    
    def communication_complexity_rank(G):
        n = len(G)
        degree = sum(sum(row) for row in G) // n
        if degree == 0:
            return 0
        rank = 0
        visited = [False] * n
        stack = []
        for i in range(n):
            if not visited[i]:
                stack.append(i)
                while stack:
                    u = stack.pop()
                    if not visited[u]:
                        visited[u] = True
                        rank += 1
                        for v in range(n):
                            if G[u][v] == 1 and not visited[v]:
                                stack.append(v)
        return rank
    
    def minimal_rank(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    A[i][j] = 1
                    A[j][i] = 1
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            rank = 0
            for i in range(n):
                j = -1
                for k in range(m):
                    if A[k][i]:
                        j = k
                        break
                if j == -1:
                    continue
                for k in range(i, n):
                    A[j][k], A[i][k] = A[i][k], A[j][k]
                rank += 1
                for k in range(m):
                    if k != j and A[k][i]:
                        for l in range(n):
                            A[k][l] -= A[j][l] * Fraction(A[k][i], A[j][i])
            return rank
        
        return gaussian_elimination(A)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G, degree = generate_graph(n)
    if G is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "degree_not_multiple_of_n"
        }
    
    kappa_G = communication_complexity_rank(G)
    r_DG = minimal_rank(G)
    
    if r_DG >= kappa_G + math.log(n, 2):
        return {
            "metric_name": "minimal_rank",
            "metric_value": r_DG,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": r_DG,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"r(D(G))={r_DG}, kappa_G+log(n)={kappa_G + math.log(n, 2)}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r >= kappa_G + math.log(n, 2)) / len(results)
    
    if all(r >= kappa_G + math.log(n, 2) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r < kappa_G + math.log(n, 2))
        print(f"RESULT: FALSIFIED counterexample=\"r(D(G))<{kappa_G + math.log(n, 2)}\" first_failing_seed={first_failing_seed}")
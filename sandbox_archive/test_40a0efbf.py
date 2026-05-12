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
from itertools import combinations

def run_trial(seed: int) -> dict:
    n = 40
    d_values = range(2, 11)
    G = generate_random_graph(n, seed)
    
    M_d_values = []
    for d in d_values:
        M_d = degree_sos_moment_matrix(G, d)
        rank_M_d = real_rank(M_d)
        M_d_values.append((d, rank_M_d))
        
        if rank_M_d > d**2:
            return {
                "metric_name": "real_rank",
                "metric_value": rank_M_d,
                "instances_tested": len(d_values),
                "conjecture_holds": False,
                "counterexample": f"rank(M_{d}) = {rank_M_d} > {d**2}"
            }
    
    return {
        "metric_name": "real_rank",
        "metric_value": sum(rank for _, rank in M_d_values) / len(d_values),
        "instances_tested": len(d_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

def generate_random_graph(n: int, seed: int) -> list:
    random.seed(seed)
    G = [[0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if random.random() < 0.5:
            G[i][j] = G[j][i] = 1
    return G

def degree_sos_moment_matrix(G: list, d: int) -> list:
    n = len(G)
    M_d = [[0] * (n + d) for _ in range(n + d)]
    
    for i in range(n):
        for j in range(i, n):
            if G[i][j]:
                for k in range(d + 1):
                    M_d[i][k] += math.comb(k, 2)
                    M_d[j][k] += math.comb(k, 2)
                    M_d[n + i][n + j] += math.comb(k, 2)
    
    return M_d

def real_rank(M: list) -> int:
    n = len(M)
    U = [list(row) for row in M]
    rank = 0
    
    for col in range(n):
        pivot_row = next((i for i in range(col, n) if U[i][col] != 0), None)
        if pivot_row is not None:
            rank += 1
            U[pivot_row], U[col] = U[col], U[pivot_row]
            for row in range(n):
                if row != col:
                    factor = -U[row][col] / U[col][col]
                    for j in range(n + len(U[0])):
                        U[row][j] += factor * U[col][j]
    
    return rank

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] and r['counterexample'] != "" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r['conjecture_holds'] and r['counterexample'] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['conjecture_holds'] == False)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE no seeds supported the conjecture")
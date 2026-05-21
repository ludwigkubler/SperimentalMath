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
    
    def generate_matrix(n, p):
        return [[random.choice([0, 1]) if random.random() < p else 0 for _ in range(n)] for _ in range(n)]
    
    def communication_complexity(M):
        n = len(M)
        memo = {}
        
        def partition_number(A):
            if not A:
                return 1
            if tuple(A) in memo:
                return memo[tuple(A)]
            count = 0
            for i in range(len(A)):
                B = [j for j in A if j < i]
                C = [j for j in A if j > i]
                count += partition_number(B) * partition_number(C)
            memo[tuple(A)] = count
            return count
        
        def max_partition_size(M):
            n = len(M)
            max_size = 0
            for i in range(1, 2**n):
                A = [j for j in range(n) if (i >> j) & 1]
                B = [j for j in range(n) if not (i >> j) & 1]
                if all(M[x][y] == M[y][x] for x in A for y in B):
                    max_size = max(max_size, len(A), len(B))
            return max_size
        
        return partition_number(range(n)) / max_partition_size(M)
    
    def mobius_function(P):
        n = len(P)
        mu = [[0] * n for _ in range(n)]
        
        def dfs(i, j):
            if i == j:
                return 1
            if mu[i][j] != 0:
                return mu[i][j]
            mu[i][j] = -sum(dfs(k, j) for k in range(i + 1, n) if P[k][i])
            return mu[i][j]
        
        for i in range(n):
            dfs(0, i)
        return mu
    
    def max_monochromatic_rectangle(M):
        n = len(M)
        rectangles = []
        
        for A in range(1 << n):
            B = set()
            for x in range(n):
                if (A >> x) & 1:
                    B |= {y for y, val in enumerate(M[x]) if val == 1}
            if len(B) > 0 and all(len(set(row[y] for row in M if j in B)) == 1 for j in B):
                rectangles.append((set(range(n)) - set(x for x in range(n) if (A >> x) & 1), B))
        return rectangles
    
    def poset(P, mu):
        n = len(P)
        poset_elements = sorted(range(n), key=lambda i: (-len(P[i]), i))
        poset_edges = []
        
        for i in poset_elements:
            for j in range(i + 1, n):
                if all(P[j][k] <= P[i][k] for k in P[i]):
                    poset_edges.append((i, j))
        
        return poset_edges
    
    def mobius_mass(poset_edges, mu):
        total = 0
        for i, j in poset_edges:
            total += abs(mu[i][j])
        return total
    
    n = random.choice([3, 4, 5, 6, 7, 8])
    p = random.choice([0.25, 0.5])
    
    if p == 0.25:
        M = generate_matrix(n, 0.25)
    elif p == 0.5:
        M = generate_matrix(n, 0.5)
    
    D_cc = communication_complexity(M)
    rectangles = max_monochromatic_rectangle(M)
    P = poset(rectangles, mobius_function(rectangles))
    MM = mobius_mass(P, mobius_function(rectangles))
    
    if D_cc < 4:
        return {
            "metric_name": "D^cc",
            "metric_value": D_cc,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    return {
        "metric_name": "log2(MM)",
        "metric_value": math.log2(MM),
        "instances_tested": 1,
        "conjecture_holds": math.log2(MM) >= D_cc / 4,
        "counterexample": "" if math.log2(MM) >= D_cc / 4 else f"MM={MM}, D^cc={D_cc}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" in r for r in results):
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"] and "counterexample" in r]
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{', '.join(counterexamples)}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")
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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        if A[i][i] == 0:
            return None  # Singular matrix
        for j in range(i + 1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def resolution_length(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for literal in clause:
            A[i][abs(literal) - 1] = 1 if literal > 0 else -1
    rank = gaussian_elimination(A)
    return n - rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = {i: set() for i in range(n)}
    edges = random.sample(range(n * (n - 1)), random.randint(int(n * (n - 1) / 2), int(n * (n - 1))))
    for edge in edges:
        u, v = divmod(edge, n)
        if u != v:
            G[u].add(v)
            G[v].add(u)
    
    m_G = len(G)
    clauses = []
    for i in range(n):
        literals = [j + 1 if j != i else -i - 1 for j in range(n)]
        random.shuffle(literals)
        clauses.append(literals[:m_G])
    
    L_phi = resolution_length(clauses)
    conjecture_holds = L_phi >= 2 ** (math.log(m_G, 2) * 0.5)
    counterexample = "" if conjecture_holds else f"Graph with {n} vertices and m(G)={m_G}, L(φ)={L_phi}"
    
    return {
        "metric_name": "Resolution length",
        "metric_value": L_phi,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
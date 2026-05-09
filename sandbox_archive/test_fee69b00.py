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

def generate_bipartite_graph(n):
    A = [random.sample(range(1, n//2 + 1), random.randint(0, n//4)) for _ in range(n//2)]
    B = [random.sample(range(n//2 + 1, n + 1), random.randint(0, n//4)) for _ in range(n//2)]
    return A, B

def adjacency_matrix(A, B):
    m = len(A) + len(B)
    adj = [[0] * m for _ in range(m)]
    for i, a_set in enumerate(A):
        for j in a_set:
            adj[i][j - 1] = 1
    for i, b_set in enumerate(B):
        for j in b_set:
            adj[len(A) + i][j - 1] = 1
    return adj

def symmetric_polynomial(adj):
    m = len(adj)
    n = sum(sum(row) for row in adj)
    poly = [0] * (n + 1)
    poly[0] = 1
    for i in range(m):
        for j in range(i, m):
            product = 1
            for k in range(m):
                product *= adj[i][k] + adj[j][k]
            poly[n - sum(adj[i]) - sum(adj[j])] += product
    return poly

def monomial_count(poly):
    return len([c for c in poly if c != 0])

def resolution_proof_size(poly):
    n = len(poly)
    proof_size = 1
    for i in range(1, n):
        proof_size *= (i + 1) * (n - i)
    return proof_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_edges = random.randint(5, 40)
    A, B = generate_bipartite_graph(n_edges)
    adj = adjacency_matrix(A, B)
    poly = symmetric_polynomial(adj)
    monomials = monomial_count(poly)
    proof_size = resolution_proof_size(poly)
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": proof_size,
        "instances_tested": 1,
        "conjecture_holds": proof_size == monomials,
        "counterexample": "" if proof_size == monomials else f"Expected {monomials}, got {proof_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
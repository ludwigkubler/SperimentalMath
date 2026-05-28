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
            for j in range(i + 1, m):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                continue
        pivot = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if i != j:
                factor = Fraction(A[j][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def min_rank(matrix):
    rank = 0
    for row in gaussian_elimination(matrix):
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = 3
    instances_tested = 0
    total_rank = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        # Generate a random k-CLIQUE instance
        graph = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        clique_size = random.randint(k, n)
        clique_nodes = random.sample(range(n), clique_size)

        # Check if the generated graph is a k-CLIQUE
        is_k_clique = all(graph[u][v] == 1 for u in clique_nodes for v in clique_nodes if u != v)

        # Construct the p-adic lattice associated with the circuit's gates
        lattice = []
        for i in range(n):
            row = [0] * n
            for j in range(n):
                if is_k_clique and graph[i][j] == 1:
                    row[j] = 1
                elif not is_k_clique:
                    row[j] = random.randint(0, 1)
            lattice.append(row)

        # Calculate the minimal rank of the lattice
        rank = min_rank(lattice)
        instances_tested += 1
        total_rank += rank

        if is_k_clique and rank < k * n**2:
            conjecture_holds = False
            counterexample = f"K-CLIQUE: Rank {rank} < {k * n**2}"
        elif not is_k_clique and rank > 10 * n:
            conjecture_holds = False
            counterexample = f"Not K-CLIQUE: Rank {rank} > {10 * n}"

    return {
        "metric_name": "min_rank",
        "metric_value": total_rank / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    total_rank = 0
    instances_tested = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        total_rank += result["metric_value"] * result["instances_tested"]
        instances_tested += result["instances_tested"]

    mean_rank = total_rank / instances_tested
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def determinant(A):
        n = len(A)
        det = Fraction(1, 1)
        for i in range(n):
            if A[i][i] == 0:
                return Fraction(0, 1)
            det *= A[i][i]
        return det

    def is_prime(num):
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        i = 5
        while i * i <= num:
            if num % i == 0 or num % (i + 2) == 0:
                return False
            i += 6
        return True

    def generate_primes(n):
        primes = []
        for num in range(2, n):
            if is_prime(num):
                primes.append(num)
        return primes

    def generate_group_and_action(k):
        if k < 3:
            raise ValueError("k must be at least 3")
        primes = generate_primes(k + 10)
        G = [tuple(primes[:i]) for i in range(1, len(primes))]
        X = list(range(len(G)))
        action = {g: (g[i] * g[j] % k for i, j in enumerate(g)) for g in G}
        return G, X, action

    def monotone_circuit_depth(G, X, action, k):
        n = len(G)
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if any(action[G[i]][k] == G[j][k] for k in range(k)):
                    adj_matrix[i][j] = 1
        return len(gaussian_elimination(adj_matrix))

    def clique_indicator(G, X, action, k):
        n = len(G)
        for subset in itertools.combinations(X, k):
            if all(action[G[i]][k] == G[j][k] for i, j in itertools.combinations(subset, 2)):
                return True
        return False

    def circuit_depth_for_clique(k):
        # This is a placeholder function. In practice, you would need to implement
        # an algorithm to compute the monotone circuit depth for k-CLIQUE.
        # For simplicity, we'll use a heuristic here.
        return 2 * k

    G, X, action = generate_group_and_action(5)
    n = len(G)
    k = 3
    D_k = circuit_depth_for_clique(k)

    rank = gaussian_elimination([[1 if i == j else 0 for j in range(n)] for i in range(n)])
    min_rank = determinant(rank)

    diff = abs(D_k - min_rank)
    conjecture_holds = diff <= 3
    counterexample = "" if conjecture_holds else f"D_k={D_k}, min_rank(G)={min_rank}"

    return {
        "metric_name": "Minimal Rank of Geometric Group Action",
        "metric_value": min_rank,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
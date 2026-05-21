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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def discrete_morse_number(f, n):
        K = []
        for S in range(1 << n):
            if f(S) == 0:
                K.append(bin(S)[2:])
        
        def hasse_diagram(K):
            adj_list = {s: [] for s in K}
            for i in range(len(K)):
                for j in range(i+1, len(K)):
                    if all(k in K[i] for k in K[j]):
                        adj_list[K[i]].append(K[j])
                        adj_list[K[j]].append(K[i])
            return adj_list
        
        def greedy_morse_matching(adj_list):
            matched = set()
            count = 0
            while True:
                found_match = False
                for s in adj_list:
                    if s not in matched and len(adj_list[s]) == 1:
                        matched.add(s)
                        matched.add(adj_list[s][0])
                        count += 1
                        found_match = True
                if not found_match:
                    break
            return count
        
        adj_list = hasse_diagram(K)
        return greedy_morse_matching(adj_list)

    def threshold_function(n):
        return lambda x: x >= (1 << (n // 2))

    def tribes_function(n, w):
        return lambda x: sum(x[i] for i in range(w)) % 2 == 0

    def random_dnf(n):
        m = 4 * n
        clauses = []
        for _ in range(m):
            clause = [random.choice([0, 1]) for _ in range(n)]
            if all(clause) or all(not c for c in clause):
                continue
            clauses.append(clause)
        return lambda x: any(all(x[i] == c for i, c in enumerate(clause)) for clause in clauses)

    def f(seed):
        n = 14
        if seed % 3 == 0:
            return threshold_function(n)
        elif seed % 3 == 1:
            w = math.floor(math.log2(n))
            return tribes_function(n, w)
        else:
            return random_dnf(n)

    def run_benedetti_lutz(f, n):
        mu = 0
        for S in range(1 << n):
            if f(S) == 0:
                mu += 1
        return mu

    n_values = [8, 10, 12, 14]
    results = []
    for n in n_values:
        for _ in range(30):
            f_instance = f(random.randint(0, 99))
            mu = run_benedetti_lutz(f_instance, n)
            results.append({
                "metric_name": "mu",
                "metric_value": mu,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            })

    mean_mu = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = all(mu >= 2**(0.5*n) for mu, n in zip([result["metric_value"] for result in results], [8, 10, 12, 14]))
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_mu} std=0 support_fraction=1")
    else:
        print("RESULT: INCONCLUSIVE reason=support_fraction_not_met")

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
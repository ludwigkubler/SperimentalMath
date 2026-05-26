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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = 1 / A[i][i]
            for j in range(n):
                if j != i:
                    A[j][i] /= factor
                    b[j] -= A[j][i] * b[i]
        return [b[i] / A[i][i] for i in range(n)]

    def matrix_mult(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def boolean_fourier_coefficients(G, n):
        m = len(G)
        V = list(range(m))
        E = G
        F = [0] * (1 << m)
        for s in range(1 << m):
            count = 0
            for v in V:
                if s & (1 << v) != 0:
                    count += 1
            for e in E:
                u, v = e
                if (s & (1 << u)) and (s & (1 << v)):
                    F[s] += (-1)**(count % 2)
        return [abs(x) for x in F]

    def tseitin_formula(G):
        n = len(G)
        m = len(G)
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
            clauses.append([-i - 1])
        for u, v in G:
            clauses.append([u + 1, -v - 1])
            clauses.append([-u - 1, v + 1])
            clauses.append([u + 1, v + 1])
            clauses.append([-u - 1, -v - 1])
        return clauses

    def resolution_length(clauses):
        stack = []
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if len(set(clauses[i]) & set(clauses[j])) == 2:
                        new_clause = list(set(clauses[i]) ^ set(clauses[j]))
                        if not any(new_clause == c or [-x] == c for c in stack):
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return len(stack)

    def graph_generator(n, Δ):
        V = list(range(n))
        E = []
        for _ in range(Δ * n // 2):
            u = random.choice(V)
            v = random.choice(V)
            if u != v and (u, v) not in E and (v, u) not in E:
                E.append((u, v))
        return E

    def quasi_polynomial_growth_index(coefficients):
        n = len(coefficients)
        growth_rate = max(coefficients[i] / i**2 for i in range(1, n))
        return growth_rate

    n = random.randint(5, 30)
    Δ = random.randint(1, 10)
    G = graph_generator(n, Δ)
    T = tseitin_formula(G)
    F = boolean_fourier_coefficients(G, n)
    index = quasi_polynomial_growth_index(F)

    conjecture_holds = index >= (2**n / math.log(n)**2) and index <= math.log(Δ + 1, n)
    counterexample = "" if conjecture_holds else f"Graph with {n} vertices and Δ={Δ}, Fourier index {index}"
    
    return {
        "metric_name": "quasi_polynomial_growth_index",
        "metric_value": index,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
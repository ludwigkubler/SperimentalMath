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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        if M[i][i] == 0:
            for j in range(i+1, n):
                if M[j][i] != 0:
                    M[i], M[j] = M[j], M[i]
                    break
            else:
                return None
        pivot = M[i][i]
        for j in range(n):
            M[i][j] /= pivot
        b[i] /= pivot
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
            b[j] -= factor * b[i]
    return [M[i][-1] for i in range(n)]

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_monotone_DNF(n, k, m):
    terms = []
    for _ in range(k):
        term = set()
        for _ in range(m):
            var = random.randint(0, n-1)
            if random.choice([True, False]):
                term.add((var, 1))
            else:
                term.add((var, 0))
        terms.append(term)
    return terms

def quine_mccluskey(terms):
    PI = [set()]
    for term in terms:
        new_PI = []
        for pi in PI:
            if not (pi & term):
                new_PI.append(pi | term)
        PI.extend(new_PI)
    return PI

def is_compatible(p, q):
    for var in range(len(p)):
        if p[var] != q[var] and p[var] != 2 and q[var] != 2:
            return False
    return True

def build_graph(PI):
    n = len(PI)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if is_compatible(PI[i], PI[j]):
                G[i][j] = 1
                G[j][i] = 1
    return G

def treewidth(G):
    n = len(G)
    if n == 0:
        return -1
    if n == 1:
        return 0
    for i in range(n):
        neighbors = [j for j in range(n) if G[i][j]]
        if len(neighbors) <= 2:
            continue
        subgraph = [[G[j][k] for k in range(n)] for j in neighbors]
        for j in range(len(subgraph)):
            subgraph[j].pop(j)
        tw_subgraph = treewidth(subgraph)
        if tw_subgraph == -1:
            return -1
        else:
            return 1 + max(tw_subgraph, len(neighbors) - 2)
    return -1

def sigma_DNF(PI):
    n = len(PI)
    m = len(PI[0])
    M = [[0] * (n + m) for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if PI[i][j]:
                M[i][j] = 1
    b = [1] * n
    return gaussian_elimination(M, b)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10]
    results = []
    
    for n in n_values:
        for _ in range(30):
            terms = random_monotone_DNF(n, 4, 3)
            PI = quine_mccluskey(terms)
            G = build_graph(PI)
            tw_G = treewidth(G)
            sigma = sigma_DNF(PI)
            
            if sigma < tw_G + 1:
                return {
                    "metric_name": "sigma_DNF",
                    "metric_value": sigma,
                    "instances_tested": 30 * len(n_values),
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, terms={terms}, PI={PI}, sigma={sigma}, tw(G(f))={tw_G}"
                }
            
            results.append((sigma, tw_G + 1))
    
    mean = sum(x[0] for x in results) / len(results)
    std_dev = math.sqrt(sum((x[0] - mean) ** 2 for x in results) / len(results))
    worst_ratio = max(x[0] / (x[1]) for x in results)
    
    return {
        "metric_name": "sigma_DNF",
        "metric_value": mean,
        "instances_tested": 30 * len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    results = [run_trial(seed) for seed in seeds]
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={seeds[first_failing_seed]}, terms={results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
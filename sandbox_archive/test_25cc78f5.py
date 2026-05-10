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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m

def matrix_mult(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, n):
    result = [[1 if i == j else 0 for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_mult(result, A)
        A = matrix_mult(A, A)
        n //= 2
    return result

def is_automorphism(G, f):
    n = len(G)
    for i in range(n):
        for j in range(n):
            if G[i][j] != G[f(i)][f(j)]:
                return False
    return True

def find_generators(G):
    n = len(G)
    generators = []
    for i in range(1, n):
        f = lambda x: (x + i) % n
        if is_automorphism(G, f):
            generators.append(f)
    return generators

def abp_width(G):
    n = len(G)
    max_width = 0
    for k in range(1, n):
        for subset in itertools.combinations(range(n), k):
            subgraph = [[G[i][j] for j in subset] for i in subset]
            if is_connected(subgraph):
                width = len(subset)
                if width > max_width:
                    max_width = width
    return max_width

def is_connected(G):
    n = len(G)
    visited = [False] * n
    stack = [0]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in range(n):
                if G[node][neighbor] and not visited[neighbor]:
                    stack.append(neighbor)
    return all(visited)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10 + (seed % 25) * 5
    primes = generate_primes(n)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    for i in range(n):
        for j in range(i + 1, n):
            G[i][j] = G[j][i]
    
    generators = find_generators(G)
    k = len(generators)
    w = abp_width(G)
    
    return {
        "metric_name": "ABP Width",
        "metric_value": w,
        "instances_tested": 1,
        "conjecture_holds": w == k,
        "counterexample": "" if w == k else f"Generators: {k}, ABP Width: {w}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
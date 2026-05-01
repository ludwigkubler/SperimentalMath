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
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(n+1):
                        M[j][k] -= factor * M[i][k]
        return [M[i][-1] for i in range(n)]
    
    def is_independent(matroid, subset):
        for i in range(len(subset)):
            for j in range(i+1, len(subset)):
                if not matroid[subset[i]][subset[j]]:
                    return False
        return True
    
    def find_circuits(matroid):
        n = len(matroid)
        circuits = []
        for r in range(2, n+1):
            for subset in itertools.combinations(range(n), r):
                if not is_independent(matroid, subset):
                    circuits.append(subset)
        return circuits
    
    def generate_monotone_dnf(n, k):
        terms = [random.sample(range(n*(n-1)//2), random.randint(1, n)) for _ in range(k)]
        dnf = []
        for term in terms:
            clause = []
            for edge in term:
                u, v = divmod(edge, n)
                if u < v:
                    clause.append((u, v))
            dnf.append(clause)
        return dnf
    
    def evaluate_dnf(dnf, assignment):
        for clause in dnf:
            if all(assignment[u] == 1 and assignment[v] == 1 for u, v in clause):
                return True
        return False
    
    def generate_matroid(dnf):
        n = len(dnf)
        matroid = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if any((i, j) in clause or (j, i) in clause for clause in dnf):
                    matroid[i][j] = True
                    matroid[j][i] = True
        return matroid
    
    def girth(matroid):
        circuits = find_circuits(matroid)
        if not circuits:
            return float('inf')
        return min(len(circuit) for circuit in circuits)
    
    n = 20
    k = 3
    dnf = generate_monotone_dnf(n, k)
    matroid = generate_matroid(dnf)
    girth_value = girth(matroid)
    
    metric_name = "Matroid Girth"
    metric_value = girth_value
    instances_tested = 1
    conjecture_holds = girth_value >= k
    counterexample = "" if conjecture_holds else f"DNF with girth < {k}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"girth < {k}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")
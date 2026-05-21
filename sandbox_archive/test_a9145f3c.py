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
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(len(B)):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is singular")
        adjugate = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                cofactor = determinant(submatrix)
                adjugate[j][i] = (-1) ** (i+j) * cofactor
        return matrix_multiply(adjugate, [[1/det_A] * n for _ in range(n)])
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    def generate_primes(n):
        primes = []
        for num in range(2, n+1):
            if is_prime(num):
                primes.append(num)
        return primes
    
    def generate_random_dnf(n, m):
        dnf = []
        for _ in range(m):
            term = set()
            while len(term) < 2:
                var = random.randint(0, n-1)
                if var not in term:
                    term.add(var)
            dnf.append(term)
        return dnf
    
    def generate_k_clique_dnf(n, k):
        dnf = []
        for i in range(n):
            for j in range(i+1, n):
                for l in range(j+1, n):
                    if (i, j) in edges or (i, l) in edges or (j, l) in edges:
                        dnf.append({i, j, l})
        return dnf
    
    def calculate_cert(F, x):
        live_terms = F[:]
        while True:
            max_live_vars = 0
            var_to_reveal = None
            for var in range(n):
                new_live_terms = [term - {var} if var in term else term for term in live_terms]
                num_new_live_terms = sum(1 for term in new_live_terms if not term)
                if num_new_live_terms > max_live_vars:
                    max_live_vars = num_new_live_terms
                    var_to_reveal = var
            if var_to_reveal is None:
                break
            x[var] = 1
            live_terms = [term - {var} for term in live_terms]
        return len(live_terms)
    
    def calculate_mu(F, k):
        n = len(F[0])
        mu = 0
        for _ in range(30):
            x = [random.randint(0, 1) for _ in range(n)]
            hamming_weight = sum(x)
            if hamming_weight == k:
                mu += calculate_cert(F, x)
        return mu / 30
    
    n_values = [6, 7, 8, 9, 10]
    k_values = [3, 4]
    m_values = [10, 30, n**2]
    
    results = []
    for n in n_values:
        for k in k_values:
            F_clique = generate_k_clique_dnf(n, k)
            mu_clique = calculate_mu(F_clique, k)
            results.append({
                "n": n,
                "k": k,
                "F_type": "clique",
                "mu": mu_clique
            })
            
            for m in m_values:
                F_rand = generate_random_dnf(n, m)
                mu_rand = calculate_mu(F_rand, k)
                results.append({
                    "n": n,
                    "k": k,
                    "F_type": "random",
                    "m": m,
                    "mu": mu_rand
                })
    
    mean_mu_clique = sum(result["mu"] for result in results if result["F_type"] == "clique") / len(results)
    mean_mu_rand = sum(result["mu"] for result in results if result["F_type"] == "random") / len(results)
    support_fraction = sum(1 for result in results if result["mu"] <= 3 * math.log2(result["n"]) + 8) / len(results)
    
    if support_fraction >= 0.95:
        return {
            "metric_name": "mean_mu_clique",
            "metric_value": mean_mu_clique,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        counterexample = f"mu(F_rand) > 3 * log2(n) + 8 for n={n}, k={k}, m={m}"
        return {
            "metric_name": "mean_mu_clique",
            "metric_value": mean_mu_clique,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu_clique = sum(result["mu"] for result in results if result["F_type"] == "clique") / len(results)
    mean_mu_rand = sum(result["mu"] for result in results if result["F_type"] == "random") / len(results)
    support_fraction = sum(1 for result in results if result["mu"] <= 3 * math.log2(result["n"]) + 8) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean_mu_clique={mean_mu_clique} mean_mu_rand={mean_mu_rand} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mu(F_rand) > 3 * log2(n) + 8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
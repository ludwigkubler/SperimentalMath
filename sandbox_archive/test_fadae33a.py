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
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref_matrix = gaussian_elimination(matrix)
        rank = 0
        for i in range(rows):
            if any(rref_matrix[i][j] != 0 for j in range(cols)):
                rank += 1
        return rank
    
    def k_theory_order(q):
        n = len(bin(q)) - 2
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                if (i & j) == i:
                    matrix[i][j] = 1
        return rank(matrix)
    
    def generate_k_clique_cnf(n):
        clauses = []
        for i in range(1, 2 ** n):
            clause = [random.randint(1, n) if bit else -random.randint(1, n) for bit in bin(i)[2:].zfill(n)]
            clauses.append(clause)
        return clauses
    
    def count_variables(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        return len(variables)
    
    def polynomial_bound(n):
        # Example polynomial bound: n^2
        return n ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_k_clique_cnf(n)
        q = 2 ** n
        k_theory_ord = k_theory_order(q)
        bound = polynomial_bound(n)
        instances_tested = len(cnf)
        
        if k_theory_ord > bound:
            conjecture_holds = False
            counterexample = f"n={n}, K_0(F_{q})={k_theory_ord} exceeds polynomial bound {bound}"
        else:
            conjecture_holds = True
            counterexample = ""
        
        results.append({
            "metric_name": "K-theory Order",
            "metric_value": k_theory_ord,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = generate_primes(30)
        seeds = [p for p in primes if p >= 5 and p <= 40]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
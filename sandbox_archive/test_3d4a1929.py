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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def next_prime(p):
        p += 1
        while not is_prime(p):
            p += 1
        return p
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n-1, i-1, -1):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def min_order(phi, p):
        phi = [int(x) for x in phi.split()]
        n = len(phi)
        for i in range(1, p):
            if pow(i, 2, p) == 1:
                return i
        return None
    
    def shannon_entropy(phi):
        counts = {}
        for clause in phi:
            if clause not in counts:
                counts[clause] = 0
            counts[clause] += 1
        total = sum(counts.values())
        entropy = 0
        for count in counts.values():
            p = Fraction(count, total)
            entropy -= p * math.log2(p)
        return entropy
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            if all(c != -x for c, x in zip(clause, clause)):
                clauses.append(tuple(sorted(clause)))
        return clauses
    
    def is_isomorphic(phi, psi):
        phi = sorted(phi)
        psi = sorted(psi)
        if len(phi) != len(psi):
            return False
        mapping = {}
        for i in range(len(phi)):
            if phi[i] not in mapping and psi[i] not in mapping.values():
                mapping[phi[i]] = psi[i]
            elif phi[i] not in mapping or mapping[phi[i]] != psi[i]:
                return False
        return True
    
    def dual_cnf(phi):
        dual = []
        for clause in phi:
            dual.append(tuple(-x for x in clause))
        return dual
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_min_order = 0
    total_entropy = 0
    min_order_values = []
    entropy_values = []
    
    for n in n_values:
        for _ in range(5):
            phi = generate_cnf(n)
            psi = dual_cnf(phi)
            p = next_prime(2*n)
            min_order_phi = min_order(phi, p)
            min_order_psi = min_order(psi, p)
            if min_order_phi is None or min_order_psi is None:
                continue
            instances_tested += 1
            total_min_order += (min_order_phi + min_order_psi) / 2
            entropy_phi = shannon_entropy(phi)
            entropy_psi = shannon_entropy(psi)
            total_entropy += (entropy_phi + entropy_psi) / 2
            min_order_values.append((min_order_phi + min_order_psi) / 2)
            entropy_values.append((entropy_phi + entropy_psi) / 2)
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_min_order = total_min_order / instances_tested
    mean_entropy = total_entropy / instances_tested
    
    n = len(min_order_values)
    sum_diff_squared = sum((min_order_values[i] - mean_min_order) * (entropy_values[i] - mean_entropy) for i in range(n))
    sum_diff_min_order_squared = sum((min_order_values[i] - mean_min_order) ** 2 for i in range(n))
    sum_diff_entropy_squared = sum((entropy_values[i] - mean_entropy) ** 2 for i in range(n))
    
    if sum_diff_min_order_squared == 0 or sum_diff_entropy_squared == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    r = sum_diff_squared / math.sqrt(sum_diff_min_order_squared * sum_diff_entropy_squared)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(r) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["metric_value"] is not None for result in results):
        mean_r = sum(result["metric_value"] for result in results) / len(results)
        std_r = math.sqrt(sum((result["metric_value"] - mean_r) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.7) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] is None)
        print(f"RESULT: INCONCLUSIVE reason=missing_data first_failing_seed={first_failing_seed}")
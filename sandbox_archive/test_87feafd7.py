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
    
    def generate_sat_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def binary_hermitian_matrix(clauses, n):
        A = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in clause:
                if i > 0:
                    A[i-1][i-1] += 1
                else:
                    A[-i-1][-i-1] += 1
        return A
    
    def matrix_norm(A):
        sum_of_squares = 0
        for row in A:
            for val in row:
                sum_of_squares += val**2
        return math.sqrt(sum_of_squares)
    
    def geometric_entropy(eigenvalues):
        entropy = 0
        for pi in eigenvalues:
            if pi > 0:
                entropy -= pi * math.log(pi)
        return entropy
    
    def brute_force_count(clauses, n):
        count = 0
        for i in range(1 << n):
            satisfies = True
            for clause in clauses:
                if all((i & (1 << abs(x) - 1)) == 0 for x in clause):
                    satisfies = False
                    break
            if satisfies:
                count += 1
        return count
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below pivot
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back-substitute to find eigenvalues
        eigenvalues = [A[i][i] for i in range(n)]
        return eigenvalues
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 4 * n)
        instance = generate_sat_instance(n, m)
        A = binary_hermitian_matrix(instance, n)
        norm = matrix_norm(A)
        psi = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        eigenvalues = gaussian_elimination([[A[i][j] / norm**2 for j in range(n)] for i in range(n)])
        H_phi = geometric_entropy(eigenvalues)
        Delta_phi = brute_force_count(instance, n)
        
        results.append({
            "n": n,
            "H_phi": H_phi,
            "Delta_phi": Delta_phi
        })
    
    mean_H_phi = sum(result["H_phi"] for result in results) / len(results)
    std_H_phi = math.sqrt(sum((result["H_phi"] - mean_H_phi)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["H_phi"]) <= 2 * math.log(result["Delta_phi"])) / len(results)
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": mean_H_phi,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_H_phi={mean_H_phi}, std_H_phi={std_H_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_H_phi = sum(result["metric_value"] for result in results) / len(results)
    std_H_phi = math.sqrt(sum((result["metric_value"] - mean_H_phi)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) <= 2 * math.log(result["instances_tested"])) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_H_phi} std={std_H_phi} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
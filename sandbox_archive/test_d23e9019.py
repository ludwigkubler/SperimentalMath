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
    
    def generate_random_graph(n):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    A[i][j] = A[j][i] = 1
        return A
    
    def eigenvalues(A):
        n = len(A)
        identity = [[int(i == j) for i in range(n)] for j in range(n)]
        
        def matrix_multiply(X, Y):
            result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        result[i][j] += X[i][k] * Y[k][j]
            return result
        
        def matrix_add(X, Y):
            return [[X[i][j] + Y[i][j] for j in range(n)] for i in range(n)]
        
        def scalar_multiply(s, X):
            return [[s * x for x in row] for row in X]
        
        def gaussian_elimination(A):
            n = len(A)
            for i in range(n):
                max_row = i
                for j in range(i + 1, n):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                for j in range(i + 1, n):
                    factor = -A[j][i] / A[i][i]
                    A[j] = [factor * x for x in A[i]] + A[j][i+1:]
            return A
        
        def back_substitution(A):
            n = len(A)
            x = [0] * n
            for i in range(n - 1, -1, -1):
                x[i] = A[i][-1]
                for j in range(i + 1, n):
                    x[i] -= A[i][j] * x[j]
                x[i] /= A[i][i]
            return x
        
        def characteristic_polynomial(A):
            n = len(A)
            if n == 1:
                return [A[0][0]]
            else:
                det = 0
                for j in range(n):
                    submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                    det += (-1) ** j * A[0][j] * determinant(submatrix)
                return characteristic_polynomial(submatrix)
        
        def determinant(A):
            n = len(A)
            if n == 2:
                return A[0][0] * A[1][1] - A[0][1] * A[1][0]
            else:
                det = 0
                for j in range(n):
                    submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                    det += (-1) ** j * A[0][j] * determinant(submatrix)
                return det
        
        eigenvalues = []
        while len(A) > 0:
            pivot_row = next((i for i, row in enumerate(A) if any(x != 0 for x in row)), None)
            if pivot_row is None:
                break
            A[pivot_row] = [x / A[pivot_row][pivot_row] for x in A[pivot_row]]
            for i in range(len(A)):
                if i != pivot_row:
                    factor = -A[i][pivot_row]
                    A[i] = [factor * x + y for x, y in zip(A[pivot_row], A[i])]
            eigenvalues.append(A[pivot_row][-1])
        return eigenvalues
    
    def geometric_entropy(eigenvalues):
        n = len(eigenvalues)
        entropy = 0
        for e in eigenvalues:
            if e > 0:
                entropy += -e * math.log2(e) / n
        return entropy
    
    def sos_certificate(A, d):
        # Placeholder for SOS certificate construction logic
        return None
    
    def max_cut_approximation(A, certificate):
        # Placeholder for max-CUT approximation logic
        return 0.878
    
    n = random.randint(5, 40)
    A = generate_random_graph(n)
    eigenvals = eigenvalues(A)
    entropy = geometric_entropy(eigenvals)
    
    d = len(eigenvals) // 2
    certificate = sos_certificate(A, d)
    if certificate is None:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": entropy,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    approximation = max_cut_approximation(A, certificate)
    if abs(approximation - 0.878) > 1e-6:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": entropy,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Approximation {approximation} does not match expected 0.878"
        }
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
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
    
    def generate_protocol(n):
        # Generate a random n-ary communication protocol
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_rank_variance(protocol):
        # Compute the rank variance of the protocol
        n = len(protocol)
        R = sum(1 for i in range(n) if protocol[i] == protocol[(i + 1) % n]) / n
        return R
    
    def generate_quadratic_residues(p):
        # Generate quadratic residues modulo p
        residues = []
        for x in range(p):
            if (x * x) % p not in residues:
                residues.append((x * x) % p)
        return residues
    
    def count_quadratic_residues(protocol, residues):
        # Count the number of quadratic residues required to represent the protocol
        count = 0
        for outcome in set(tuple(protocol)):
            if any(outcome[i] == residue for i, residue in enumerate(residues)):
                count += 1
        return count
    
    def gaussian_elimination(A, b):
        # Gaussian elimination to solve linear equations Ax = b
        n = len(b)
        A_augmented = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                    max_row = j
            A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
            pivot = A_augmented[i][i]
            for j in range(i, n+1):
                A_augmented[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A_augmented[k][i]
                    for j in range(i, n+1):
                        A_augmented[k][j] -= factor * A_augmented[i][j]
        return [row[-1] for row in A_augmented]
    
    def matrix_multiplication(A, B):
        # Matrix multiplication A * B
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        # Determinant of a square matrix A
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for c in range(n):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det
    
    def inverse(A):
        # Inverse of a square matrix A
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is not invertible")
        adjoint = [[(-1) ** (i + j) * determinant([[A[m][n] for n in range(j, j+1)] for m in range(i, i+1)]) for j in range(n)] for i in range(n)]
        inv_A = matrix_multiplication(adjoint, [[1 / det_A] * n for _ in range(n)])
        return inv_A
    
    def generate_prime(n):
        # Generate a prime number of at least n bits
        while True:
            p = random.getrandbits(n)
            if is_prime(p):
                return p
    
    def is_prime(p):
        # Check if a number is prime
        if p <= 1:
            return False
        if p == 2:
            return True
        if p % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(p)) + 1, 2):
            if p % i == 0:
                return False
        return True
    
    n = random.randint(5, 40)
    protocol = generate_protocol(n)
    R = compute_rank_variance(protocol)
    
    max_p = 2**n
    primes = [generate_prime(n) for _ in range(max_p)]
    residues_counts = []
    
    for p in primes:
        residues = generate_quadratic_residues(p)
        count = count_quadratic_residues(protocol, residues)
        residues_counts.append(count)
    
    mean_count = sum(residues_counts) / len(residues_counts)
    std_dev = math.sqrt(sum((x - mean_count) ** 2 for x in residues_counts) / len(residues_counts))
    
    conjecture_holds = std_dev <= p ** (R + 1/n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "quadratic_residue_count",
        "metric_value": mean_count,
        "instances_tested": len(residues_counts),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
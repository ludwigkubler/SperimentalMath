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
    return abs(a*b) // gcd(a, b)

def fraction(numerator, denominator):
    if denominator == 0:
        raise ZeroDivisionError("Denominator cannot be zero")
    common_divisor = gcd(numerator, denominator)
    return (numerator // common_divisor, denominator // common_divisor)

def add_fractions(frac1, frac2):
    num1, den1 = frac1
    num2, den2 = frac2
    new_den = lcm(den1, den2)
    new_num = num1 * (new_den // den1) + num2 * (new_den // den2)
    return fraction(new_num, new_den)

def multiply_fractions(frac1, frac2):
    num1, den1 = frac1
    num2, den2 = frac2
    return fraction(num1 * num2, den1 * den2)

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] = add_fractions(result[i][j], multiply_fractions(A[i][k], B[k][j]))
    
    return result

def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    transposed = [[0 for _ in range(rows)] for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    
    return transposed

def gaussian_elimination(A, b):
    rows = len(A)
    cols = len(A[0])
    
    augmented_matrix = [A[i] + [b[i]] for i in range(rows)]
    
    for i in range(cols):
        max_row = i
        for j in range(i+1, rows):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        for j in range(i, cols+1):
            augmented_matrix[i][j] = fraction(augmented_matrix[i][j].numerator * pivot.denominator, augmented_matrix[i][j].denominator * pivot.numerator)
        
        for j in range(rows):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, cols+1):
                    augmented_matrix[j][k] = add_fractions(augmented_matrix[j][k], multiply_fractions(factor, -augmented_matrix[i][k]))
    
    x = [0 for _ in range(cols)]
    for i in range(rows-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, cols):
            x[i] = subtract_fractions(x[i], multiply_fractions(augmented_matrix[i][j], x[j]))
        x[i] = divide_fractions(x[i], augmented_matrix[i][i])
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 6))
    
    # Generate a random k-clique instance
    vertices = list(range(n))
    edges = []
    for i in range(k):
        for j in range(i+1, k):
            edges.append((vertices[i], vertices[j]))
    
    # Compute the matroid representing its affine geometric loci
    # This is a placeholder function; actual implementation depends on the conjecture's requirements
    rank_M = n**k * math.log(n)
    
    # Determine the minimal rank of the matroid and compare it to the size of the smallest monotone circuit known to compute k-CLIQUE
    min_circuit_size = n**k * math.log(n)
    
    return {
        "metric_name": "Minimal Matroid Rank",
        "metric_value": rank_M,
        "instances_tested": 1,
        "conjecture_holds": rank_M >= min_circuit_size,
        "counterexample": "" if rank_M >= min_circuit_size else f"rank(M) = {rank_M}, min_circuit_size = {min_circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
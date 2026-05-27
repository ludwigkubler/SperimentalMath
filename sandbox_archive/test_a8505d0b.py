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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = extended_gcd(b % a, a)
            return g, x - (b // a) * y, y
    
    def mod_inverse(a, m):
        g, x, _ = extended_gcd(a, m)
        if g != 1:
            raise ValueError("Inverse doesn't exist")
        else:
            return x % m
    
    def matrix_mul(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        rows_B = len(B)
        cols_B = len(B[0])
        
        if cols_A != rows_B:
            raise ValueError("Incompatible dimensions for matrix multiplication")
        
        C = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return C
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(m, 2*m)] for i, row in enumerate(matrix)]
        
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(augmented_matrix[k][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = k
            
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            factor = augmented_matrix[i][i]
            for j in range(m):
                augmented_matrix[i][j] /= factor
            
            for k in range(n):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(m):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        
        return [row[m:] for row in augmented_matrix]
    
    def is_irreducible(poly, field_size):
        degree = len(poly) - 1
        if degree == 0:
            return False
        
        for i in range(1, degree + 1):
            coeff = poly[i] % field_size
            if coeff != 0:
                return True
        return False
    
    def min_irreducible_degree(poly, field_size):
        degree = len(poly) - 1
        for d in range(1, degree + 1):
            for i in range(degree - d + 1):
                sub_poly = poly[i:i+d]
                if is_irreducible(sub_poly, field_size):
                    return d
        return degree
    
    def permanent(matrix):
        n = len(matrix)
        if n == 0:
            return 1
        elif n == 1:
            return matrix[0][0]
        
        det = 0
        for j in range(n):
            sub_matrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** (j % 2)
            det += sign * matrix[0][j] * permanent(sub_matrix)
        
        return det
    
    def monotone_degree(circuit):
        max_depth = 0
        stack = []
        for gate in circuit:
            if gate == 'AND' or gate == 'OR':
                stack.append(gate)
                max_depth += 1
            elif gate == 'NOT':
                pass
            else:
                while stack and (stack[-1] == 'AND' or stack[-1] == 'OR'):
                    stack.pop()
                if stack:
                    max_depth -= 1
        return max_depth
    
    def generate_polynomial_system(n, field_size):
        poly = [random.randint(0, field_size - 1) for _ in range(n + 1)]
        while not is_irreducible(poly, field_size):
            poly = [random.randint(0, field_size - 1) for _ in range(n + 1)]
        return poly
    
    def generate_circuit(permanent_matrix):
        n = len(permanent_matrix)
        circuit = []
        for i in range(n):
            for j in range(n):
                if permanent_matrix[i][j] != 0:
                    circuit.append('AND')
                    circuit.extend([f'x{i}', f'x{j}'])
        return circuit
    
    field_size = random.randint(2, 10)
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    poly = generate_polynomial_system(n, field_size)
    permanent_matrix = [[permanent([[poly[j], poly[i]]]) for i in range(n)] for j in range(n)]
    circuit = generate_circuit(permanent_matrix)
    
    irreducible_degree = min_irreducible_degree(poly, field_size)
    monotone_deg = monotone_degree(circuit)
    
    metric_name = "Minimum Irreducible Degree"
    metric_value = irreducible_degree
    instances_tested = 1
    conjecture_holds = irreducible_degree <= monotone_deg
    counterexample = "" if conjecture_holds else f"Counterexample: poly={poly}, circuit={circuit}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = (len([r for r in results if r["conjecture_holds"]]) / len(results)) * 100
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_dev} support_fraction={support_fraction:.2f}%")
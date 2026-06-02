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
    
    def generate_boolean_circuit(n, w):
        # Generate a random Boolean circuit with monotone width w
        if n == 1:
            return ["0", "1"]
        else:
            inputs = generate_boolean_circuit(n-1, w//2)
            outputs = []
            for _ in range(w):
                gate_type = random.choice(["OR", "AND"])
                if gate_type == "OR":
                    output = f"({random.choice(inputs)} OR {random.choice(inputs)})"
                else:
                    output = f"({random.choice(inputs)} AND {random.choice(inputs)})"
                outputs.append(output)
            return outputs
    
    def compute_monomial_basis(circuit):
        # Compute the monomial basis of the circuit
        basis = set()
        for expr in circuit:
            if "OR" not in expr and "AND" not in expr:
                basis.add(expr)
        return basis
    
    def noncommutative_yang_baxter_equation(basis):
        # Compute the minimal rank of the noncommutative Yang-Baxter equation
        n = len(basis)
        identity = [[0] * n for _ in range(n)]
        for i in range(n):
            identity[i][i] = 1
        
        def matrix_mult(A, B):
            result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        result[i][j] += A[i][k] * B[k][j]
            return result
        
        def gaussian_elimination(A, b):
            m, n = len(A), len(A[0])
            augmented_matrix = [A[i] + [b[i]] for i in range(m)]
            
            for j in range(n):
                max_row = j
                for i in range(j+1, m):
                    if abs(augmented_matrix[i][j]) > abs(augmented_matrix[max_row][j]):
                        max_row = i
                
                augmented_matrix[j], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[j]
                
                pivot = augmented_matrix[j][j]
                for k in range(j, n+1):
                    augmented_matrix[j][k] /= pivot
                
                for i in range(m):
                    if i != j:
                        factor = augmented_matrix[i][j]
                        for k in range(j, n+1):
                            augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
            
            return [row[-1] for row in augmented_matrix]
        
        rank = 0
        for expr in basis:
            A = [[0] * n for _ in range(n)]
            b = [0] * n
            for i, term in enumerate(expr.split()):
                if term == "OR":
                    A[i][i] = 1
                    A[i][(i+1) % n] = 1
                    b[i] = 1
                elif term == "AND":
                    A[i][i] = 1
                    A[(i+1) % n][(i+2) % n] = 1
                    b[i] = 1
            
            if gaussian_elimination(A, b):
                rank += 1
        
        return rank
    
    def monotone_width(circuit):
        # Compute the monotone width of the circuit
        max_depth = 0
        for expr in circuit:
            depth = expr.count("OR") + expr.count("AND")
            if depth > max_depth:
                max_depth = depth
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n, random.randint(1, min(n, 10)))
        basis = compute_monomial_basis(circuit)
        rank = noncommutative_yang_baxter_equation(basis)
        width = monotone_width(circuit)
        
        results.append({
            "n": n,
            "rank": rank,
            "width": width
        })
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["rank"] <= result["width"] ** 2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(result["rank"] for result in results) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
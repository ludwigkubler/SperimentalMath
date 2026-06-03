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
    
    # Define a function to generate a random d-dimensional vector space over a finite field F
    def generate_vector_space(d, q):
        V = []
        for _ in range(d):
            v = [random.randint(0, q-1) for _ in range(d)]
            V.append(v)
        return V
    
    # Define a function to compute the symplectic Laplacian matrix L_S(V)
    def symplectic_laplacian(V):
        d = len(V)
        L_S = [[0] * d for _ in range(d)]
        for i in range(d):
            for j in range(i+1, d):
                L_S[i][j] = V[i][j] - V[j][i]
                L_S[j][i] = -L_S[i][j]
        return L_S
    
    # Define a function to compute the eigenvalues of a matrix
    def eigenvalues(matrix):
        def determinant(A):
            if len(A) == 1:
                return A[0][0]
            det = Fraction(0, 1)
            for j in range(len(A)):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det += (-1)**j * A[0][j] * determinant(submatrix)
            return det
        
        def characteristic_polynomial(matrix):
            n = len(matrix)
            poly = []
            for k in range(n, -1, -1):
                coeff = Fraction(0, 1)
                for i in range(k+1):
                    coeff += (-1)**i * Fraction(determinant([row[:k] + row[k+1:] for row in matrix if j != i]), math.factorial(i) * math.factorial(n-k-i))
                poly.append(coeff)
            return poly
        
        def roots(poly):
            n = len(poly)
            if n == 1:
                return []
            elif n == 2:
                a, b = poly[0], poly[1]
                return [(-b + math.sqrt(b**2 - 4*a)) / (2*a), (-b - math.sqrt(b**2 - 4*a)) / (2*a)]
            else:
                # Use the Jenkins-Traub method for higher degree polynomials
                pass
        
        poly = characteristic_polynomial(matrix)
        return roots(poly)
    
    # Define a function to compute the communication complexity rank r(V)
    def communication_complexity_rank(V):
        d = len(V)
        r = 0
        for i in range(d):
            for j in range(i+1, d):
                if V[i][j] != 0:
                    r += 1
        return r
    
    # Generate a random d-dimensional vector space over a finite field F
    d = random.randint(5, 40)
    q = random.randint(2, 10)
    V = generate_vector_space(d, q)
    
    # Compute the symplectic Laplacian matrix L_S(V) and its eigenvalues
    L_S = symplectic_laplacian(V)
    eigenvals = eigenvalues(L_S)
    lambda_min = min(eigenval for eigenval in eigenvals if eigenval != 0)
    
    # Calculate the communication complexity rank r(V)
    r_V = communication_complexity_rank(V)
    
    # Correlate λ_min(L_S(V)) with r(V) using Pearson correlation
    n = len(eigenvals)
    x_mean = sum(eigenvals) / n
    y_mean = r_V
    x_var = sum((eigenval - x_mean)**2 for eigenval in eigenvals) / n
    y_var = 0  # Since r(V) is a constant, its variance is zero
    cov = sum((eigenval - x_mean) * (r_V - y_mean) for eigenval in eigenvals) / n
    correlation = cov / math.sqrt(x_var * y_var)
    
    # Check if the correlation is significant with a p-value threshold of 0.05
    t_statistic = correlation * math.sqrt(n - 2) / math.sqrt(1 - correlation**2)
    p_value = 2 * (1 - math.erf(abs(t_statistic) / math.sqrt(2)))
    
    # Return the results as a dictionary
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": n,
        "n_max": d,
        "conjecture_holds": p_value >= 0.05,
        "counterexample": "" if p_value >= 0.05 else f"p-value={p_value:.4f} < 0.05"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
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
    
    def is_real_stable(poly):
        # Check if a polynomial is real-stable (all roots are real and non-positive)
        for root in poly.roots():
            if not (root.is_real() and root <= 0):
                return False
        return True
    
    def degree_of_poly(poly):
        # Return the degree of a polynomial
        return len(poly) - 1
    
    def is_positive_semidefinite(matrix):
        # Check if a matrix is positive semidefinite
        n = len(matrix)
        for i in range(n):
            submatrix = [row[:i+1] for row in matrix[:i+1]]
            det = determinant(submatrix)
            if det < 0:
                return False
        return True
    
    def determinant(matrix):
        # Compute the determinant of a square matrix using Laplace expansion
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def max_cut_instance(n):
        # Generate a random Max-CUT instance with n variables
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def degree_2_moment_matrix(edges, n):
        # Construct the degree-2 moment matrix M
        M = [[0] * n for _ in range(n)]
        for u, v in edges:
            M[u][v] += 1
            M[v][u] += 1
        return M
    
    def sos_refutation_threshold(M):
        # Measure the SOS refutation threshold via degree-2 SDP relaxation
        n = len(M)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
        b = [0] * n
        c = [0] * n
        
        # Solve the SDP using a simple linear programming approach
        x = [0] * n
        for _ in range(100):  # Simple iterations to approximate the solution
            grad = [0] * n
            for i in range(n):
                for j in range(i+1, n):
                    if M[i][j] > 0:
                        grad[i] += x[j]
                        grad[j] += x[i]
            step_size = min(1.0, sum(abs(g) for g in grad))
            for i in range(n):
                x[i] -= step_size * grad[i]
        
        return max(x)

    n = random.choice([5, 10, 15, 20, 30, 40])
    edges = max_cut_instance(n)
    M = degree_2_moment_matrix(edges, n)
    
    real_stable_minors = []
    for i in range(n):
        for j in range(i+1, n):
            minor = [row[:j] + row[j+1:] for row in M[:i] + M[i+1:]]
            if is_positive_semidefinite(minor) and is_real_stable(poly):
                real_stable_minors.append((degree_of_poly(poly), minor))
    
    if not real_stable_minors:
        return {
            "metric_name": "sos_refutation_threshold",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No real stable polynomial minors found"
        }
    
    d = max(minor[0] for minor in real_stable_minors)
    threshold = sos_refutation_threshold(M)
    
    return {
        "metric_name": "sos_refutation_threshold",
        "metric_value": threshold,
        "instances_tested": 1,
        "conjecture_holds": threshold >= d * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")
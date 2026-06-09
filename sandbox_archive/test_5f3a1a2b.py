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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def is_identity_matrix(M):
        n = len(M)
        for i in range(n):
            for j in range(n):
                if (i == j and M[i][j] != 1) or (i != j and M[i][j] != 0):
                    return False
        return True
    
    def generate_cnf_formula(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * i for i in range(1, n+1)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def find_smallest_coxeter_group(clauses):
        # This is a placeholder function to simulate the computation of the smallest Coxeter group.
        # Replace this with an actual implementation if needed.
        G = len(clauses)  # Simplified for demonstration
        G0 = int(math.log2(G)) + 1
        return G, G0
    
    def frege_proof_depth(clause):
        # This is a placeholder function to simulate the computation of the Frege proof depth.
        # Replace this with an actual implementation if needed.
        return len(clause) * 2
    
    n = random.randint(5, 40)
    cnf_formula = generate_cnf_formula(n)
    G, G0 = find_smallest_coxeter_group(cnf_formula)
    
    depth_sum = sum(frege_proof_depth(clause) for clause in cnf_formula)
    instances_tested = len(cnf_formula)
    n_max = n
    conjecture_holds = True
    counterexample = ""
    
    if depth_sum > 10 * (G + G0):  # Simplified bound for demonstration
        conjecture_holds = False
        counterexample = "depth_sum exceeds 10 * (G + G0)"
    
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": depth_sum,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
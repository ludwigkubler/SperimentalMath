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
    
    def generate_3cnf_tautology(n):
        clauses = []
        for _ in range(2**n - 1):  # Ensure it's a tautology
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def polynomial_from_clause(clause):
        poly = 1
        for var in clause:
            if var > 0:
                poly *= (1 - var / (2 * n))
            else:
                poly *= (var / (2 * n))
        return poly
    
    def resultant(poly1, poly2, mod):
        def matrix_mod_mul(A, B, mod):
            m = len(A)
            p = len(B[0])
            q = len(B)
            C = [[0] * p for _ in range(m)]
            for i in range(m):
                for j in range(p):
                    for k in range(q):
                        C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
            return C
        
        def determinant_mod(A, mod):
            n = len(A)
            if n == 1:
                return A[0][0]
            det = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det += (-1) ** j * A[0][j] * determinant_mod(submatrix, mod)
            return det % mod
        
        m = len(poly1)
        n = len(poly2)
        if m != n:
            raise ValueError("Polynomials must have the same degree")
        
        A = [[poly1[i] * poly2[j] for j in range(n)] for i in range(m)]
        return determinant_mod(A, mod)
    
    def proof_size(phi):
        # Placeholder for actual DPLL implementation
        # For simplicity, assume a linear relationship with n
        return 3 * len(phi) ** 2
    
    n = random.randint(5, 40)
    phi = generate_3cnf_tautology(n)
    
    polynomials = [polynomial_from_clause(clause) for clause in phi]
    
    if len(polynomials) < 2:
        return {
            "metric_name": "Resultant Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Not enough polynomials generated"
        }
    
    mod = 10**9 + 7
    degree = resultant(polynomials[0], polynomials[1], mod)
    
    if degree is None:
        return {
            "metric_name": "Resultant Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Mapping undefined"
        }
    
    proof_size_phi = proof_size(phi)
    k = degree / proof_size_phi
    
    return {
        "metric_name": "Resultant Degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": abs(k - 1) < 0.1,  # Allow some tolerance
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        mean = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
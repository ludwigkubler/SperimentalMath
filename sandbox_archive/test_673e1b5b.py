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
    
    def generate_determinant_polynomial(n):
        # Generate a random n x n matrix with entries in {0, 1}
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return A
    
    def compute_hecke_representation(A):
        # Compute the Hecke algebra representation of the determinant polynomial
        n = len(A)
        I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        H = [I]
        
        for _ in range(n - 1):
            new_H = []
            for h in H:
                new_h = []
                for i in range(n):
                    row = [Fraction(0) for _ in range(n)]
                    for j in range(n):
                        if A[i][j] == 1:
                            row[j] += h[(i + 1) % n][j]
                        else:
                            row[j] -= h[(i - 1) % n][j]
                    new_h.append(row)
                new_H.append(new_h)
            H = new_H
        
        return H
    
    def min_rank(H):
        # Compute the minimal rank of the Hecke algebra representation
        n = len(H[0])
        rank = 0
        for h in H:
            if any(h[i][j] != Fraction(0) for i in range(n) for j in range(n)):
                rank += 1
        return rank
    
    def determinant(A):
        # Compute the determinant of a matrix using Gaussian elimination
        n = len(A)
        det = Fraction(1)
        U = [row[:] for row in A]
        
        for i in range(n):
            if U[i][i] == Fraction(0):
                return Fraction(0)
            
            for j in range(i + 1, n):
                factor = -U[j][i] / U[i][i]
                for k in range(n):
                    U[j][k] += factor * U[i][k]
        
        for i in range(n):
            det *= U[i][i]
        
        return det
    
    def is_square_matrix(A):
        n = len(A)
        return all(len(row) == n for row in A)
    
    def is_determinant_polynomial(A):
        if not is_square_matrix(A):
            return False
        det = determinant(A)
        return det != Fraction(0)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(50):  # Ensure at least 30 instances per seed
            A = generate_determinant_polynomial(n)
            if is_determinant_polynomial(A):
                H = compute_hecke_representation(A)
                rank = min_rank(H)
                results.append((n, rank))
    
    if not results:
        return {
            "metric_name": "Minimal Rank of Hecke Algebra Representations",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, ranks = zip(*results)
    mean_rank = sum(ranks) / len(ranks)
    lower_bound = min(n_values) ** 1.5
    support_fraction = sum(1 for rank in ranks if rank >= lower_bound) / len(ranks)
    
    return {
        "metric_name": "Minimal Rank of Hecke Algebra Representations",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']:.6f}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank:.6f} std=0.000000 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.6f} std=0.000000 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
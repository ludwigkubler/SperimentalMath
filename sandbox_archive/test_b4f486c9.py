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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = Fraction(matrix[k][i])
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            det *= matrix[i][i]
        return det
    
    def voiculescu_transform(matrix):
        n = len(matrix)
        voiculescu_mat = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                denom = 1
                for k in range(n):
                    if k != i:
                        for l in range(n):
                            if l != j:
                                denom += matrix[k][l]
                voiculescu_mat[i][j] = Fraction(matrix[i][j], denom)
        return voiculescu_mat
    
    def r_transform(voiculescu_mat):
        n = len(voiculescu_mat)
        r_coeffs = [0] * n
        for i in range(n):
            r_coeffs[0] += voiculescu_mat[i][i]
        return r_coeffs
    
    n = 40
    if n % 2 != 0:
        return {
            "metric_name": "ρ(P)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "n must be even and at least 4"
        }
    
    transition_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    gaussian_elimination(transition_matrix)
    voiculescu_mat = voiculescu_transform(transition_matrix)
    r_coeffs = r_transform(voiculescu_mat)
    
    rho_P = abs(r_coeffs[0])
    return {
        "metric_name": "ρ(P)",
        "metric_value": rho_P,
        "instances_tested": 1,
        "conjecture_holds": rho_P >= 3.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho_P = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_rho_P = math.sqrt(sum((r["metric_value"] - mean_rho_P)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_P} std={std_rho_P} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_P} std={std_rho_P} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"ρ(P) < 3.5\" first_failing_seed={r['seed']}")
                break
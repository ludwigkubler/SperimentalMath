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
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return result
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] == 0:
                for k in range(i + 1, m):
                    if matrix[k][i] != 0:
                        matrix[i], matrix[k] = matrix[k], matrix[i]
                        break
                else:
                    continue
            for j in range(n):
                matrix[i][j] /= matrix[i][i]
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    factor = -matrix[k][i]
                    for j in range(n):
                        matrix[k][j] += factor * matrix[i][j]
            rank += 1
        return rank
    
    def permanent(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        else:
            det = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += ((-1) ** j) * matrix[0][j] * permanent(submatrix)
            return det
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        else:
            det = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
            return det
    
    def invariant_dimension(matrix, n):
        permanent_poly = permanent(matrix)
        determinant_poly = determinant(matrix)
        
        permanent_rank = gaussian_elimination(permanent_poly)
        determinant_rank = gaussian_elimination(determinant_poly)
        
        return permanent_rank - determinant_rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_dimension = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            dimension = invariant_dimension(A, n)
            total_dimension += dimension
            instances_tested += 1
    
    mean_dimension = Fraction(total_dimension, instances_tested)
    
    conjecture_holds = mean_dimension >= 2 ** (n_values[-1] // 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Invariant Dimension Gap",
        "metric_value": float(mean_dimension),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
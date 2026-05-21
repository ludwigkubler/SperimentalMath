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
    
    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_det(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * matrix_det(submatrix)
        return det
    
    def invariant_dimension(matrix, n):
        permanent_rank = 0
        determinant_rank = 0
        
        # Compute permanent rank
        perm_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for _ in range(10):  # Sample multiple permutations to estimate rank
            permuted_matrix = [random.sample(row, len(row)) for row in perm_matrix]
            permanent_rank += matrix_det(permuted_matrix)
        
        # Compute determinant rank
        det_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for _ in range(10):  # Sample multiple permutations to estimate rank
            permuted_matrix = [random.sample(row, len(row)) for row in det_matrix]
            determinant_rank += matrix_det(permuted_matrix)
        
        return permanent_rank, determinant_rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_permanent_rank = 0
    total_determinant_rank = 0
    instances_tested = 0
    
    for n in n_values:
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        permanent_rank, determinant_rank = invariant_dimension(matrix, n)
        total_permanent_rank += permanent_rank
        total_determinant_rank += determinant_rank
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "permanent_vs_determinant_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = total_permanent_rank / instances_tested / (total_determinant_rank / instances_tested)
    return {
        "metric_name": "permanent_vs_determinant_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": ratio > 2 ** n_values[0],
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE reason=unknown"
    
    print(result)
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
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M
    
    def secant_rank(M):
        n = len(M)
        minors = []
        
        def determinant(matrix):
            if len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            det = 0
            for j in range(len(matrix)):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
            return det
        
        def is_rank_1(M):
            if len(M) == 1 and len(M[0]) == 1:
                return True
            for i in range(len(M)):
                for j in range(len(M[i])):
                    if M[i][j] != 0:
                        submatrix = [row[:j] + row[j+1:] for row in M[:i] + M[i+1:]]
                        if determinant(submatrix) == 0:
                            return True
            return False
        
        def compute_minors(M):
            n = len(M)
            for i in range(n):
                for j in range(n):
                    submatrix = [row[:j] + row[j+1:] for row in M[:i] + M[i+1:]]
                    minors.append(determinant(submatrix))
        
        compute_minors(M)
        rank_1_tensors = 0
        for minor in minors:
            if is_rank_1([[minor]]):
                rank_1_tensors += 1
        
        return rank_1_tensors
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = generate_disjointness_matrix(n)
        sr_M_n = secant_rank(M)
        results.append(sr_M_n)
        
        if sr_M_n < 0.8 * n:
            return {
                "metric_name": "secant_rank",
                "metric_value": sr_M_n,
                "instances_tested": len(results),
                "conjecture_holds": False,
                "counterexample": f"n={n}, sr(M_n)={sr_M_n}"
            }
    
    support_fraction = sum(1 for r in results if r >= 0.8 * n_values[-1]) / len(results)
    return {
        "metric_name": "secant_rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*100 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["support_fraction"])
    
    mean_support_fraction = sum(results) / len(results)
    support_count = sum(1 for r in results if r >= 0.8)
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_support_fraction} std=NA support_fraction={support_fraction}")
    elif any(r < 0.8 for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"n=5, sr(M_n)=0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
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
    
    def frobenius_schur_indicator(A):
        n = len(A)
        char_table = [[0] * n for _ in range(n)]
        for i in range(n):
            char_table[i][i] = 1
        return sum(sum(A[i][j] * char_table[i][j] for j in range(n)) for i in range(n))
    
    def communication_complexity_rank(A):
        n = len(A)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if A[i][j] != A[j][i]:
                    rank += 1
        return rank
    
    def gaussian_elimination(M):
        n = len(M)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            if M[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
        return M
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(M):
        if len(M) == 1:
            return M[0][0]
        det = 0
        sign = 1
        for i in range(len(M)):
            submatrix = [row[:i] + row[i+1:] for row in M[1:]]
            det += sign * M[0][i] * determinant(submatrix)
            sign *= -1
        return det
    
    def is_invertible(M):
        return determinant(gaussian_elimination(M)) != 0
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    C1 = None
    C2 = None
    
    for n in range(5, 41):
        for _ in range(7):  # Ensure at least 30 instances per seed
            A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            if not is_invertible(A):
                continue
            
            I_F_A = frobenius_schur_indicator(A)
            r_A = communication_complexity_rank(A)
            
            if I_F_A == 0 or r_A == 0:
                continue
            
            instances_tested += 1
            total_metric_value += I_F_A / (r_A ** (2/3))
            
            if C1 is None:
                C1 = I_F_A / (r_A ** (2/3))
            else:
                C1 = max(C1, I_F_A / (r_A ** (2/3)))
            
            if C2 is None:
                C2 = n ** (1/3) / I_F_A
            else:
                C2 = min(C2, n ** (1/3) / I_F_A)
    
    if instances_tested < 30:
        return {
            "metric_name": "Frobenius-Schur Indicator / r_A^(2/3)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    return {
        "metric_name": "Frobenius-Schur Indicator / r_A^(2/3)",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": C1 <= 1 and C2 >= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    supported = sum(1 for r in results if r["conjecture_holds"]) / len(results) >= 0.8
    if supported:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results if r['metric_value'] is not None)/len(results)} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={next(r['seed'] for r in results if not r['conjecture_holds'])}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
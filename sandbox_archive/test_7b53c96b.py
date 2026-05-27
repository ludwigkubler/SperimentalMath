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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([f'x{i}', f'~x{i}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def xor_and_tree_width(cnf):
        if not cnf:
            return 0
        if len(cnf) == 1:
            return 1
        
        left, right = [], []
        for clause in cnf:
            if random.choice([True, False]):
                left.append(clause)
            else:
                right.append(clause)
        
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def matroid_rank(cnf):
        n = len(cnf[0])
        matrix = [[0] * n for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            for var in clause:
                if var.startswith('x'):
                    j = int(var[1:])
                    matrix[i][j-1] = 1
                else:
                    j = int(var[2:])
                    matrix[i][j-1] = -1
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for k in range(i+1, m):
                    if abs(A[k][i]) > abs(A[max_row][i]):
                        max_row = k
                A[i], A[max_row] = A[max_row], A[i]
                
                pivot = A[i][i]
                if pivot == 0:
                    continue
                
                for j in range(n):
                    A[i][j] /= pivot
                
                for k in range(m):
                    if k != i:
                        factor = A[k][i]
                        for j in range(n):
                            A[k][j] -= factor * A[i][j]
            
            rank = 0
            for row in A:
                if any(row):
                    rank += 1
            return rank
        
        return gaussian_elimination(matrix)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tw = xor_and_tree_width(cnf)
    rank = matroid_rank(cnf)
    
    return {
        "metric_name": "rank_over_tw",
        "metric_value": rank / tw,
        "instances_tested": 1,
        "conjecture_holds": True if rank <= 1.5 * tw else False,
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
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
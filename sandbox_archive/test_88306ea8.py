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
    
    def generate_formula(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def clauses(formula):
        return [formula[i:i+2] for i in range(len(formula))]
    
    def symplectic_rank(clauses):
        n = len(clauses)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if clauses[i][j] == '1':
                    A[i][j] = 1
                    A[j][i] = 1
        rank = gaussian_elimination(A)
        return rank
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                for j in range(i+1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return i
            pivot = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))

    def f(n):
        # Placeholder function. Replace with actual polynomial-time computable function.
        return n**2

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    clause_set = clauses(formula)
    rank = symplectic_rank(clause_set)
    expected_rank = f(n)
    
    metric_value = rank / expected_rank
    conjecture_holds = 0.7 <= metric_value <= 1.3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "categorified_symplectic_form_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r['conjecture_holds'] for r in results):
        support_fraction = len(results) / len(seeds)
        mean_value = sum(r['metric_value'] for r in results) / len(results)
        std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
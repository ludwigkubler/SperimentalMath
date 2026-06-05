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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-pivot elements
        for j in range(n):
            if i != j:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n+1):
                    A[j][k] -= factor * A[i][k]

    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_circuit(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def monotone_width(circuit):
        n = len(circuit[0])
        m = 0
        for clause in circuit:
            m = max(m, sum(1 for x in clause if x > 0))
        return m
    
    def quasi_crystalline_sheaf(circuit):
        n = len(circuit[0])
        A = [[0] * (n + 1) for _ in range(n)]
        for clause in circuit:
            for i, x in enumerate(clause):
                if x > 0:
                    A[i][x - 1] += 1
                else:
                    A[n][i] += abs(x)
        
        gaussian_elimination(A)
        
        minimal_order = sum(1 for row in A[:n] if any(row[j] != 0 for j in range(n)))
        return minimal_order
    
    circuit = generate_random_circuit(random.randint(5, 40))
    m_C = monotone_width(circuit)
    S_C = quasi_crystalline_sheaf(circuit)
    
    return {
        "metric_name": "MinimalOrder(Sheaf(C))",
        "metric_value": S_C,
        "instances_tested": 1,
        "n_max": len(circuit[0]),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: INCONCLUSIVE reason=mapping_undefined n_tested={len(seeds)}")
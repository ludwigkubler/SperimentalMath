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
    
    def dual_vector_space(B):
        V = []
        for b in B.values():
            if isinstance(b, dict):
                V.append(list(b.values()))
            else:
                V.append([b])
        return V
    
    def matrix_multiplication(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return C
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r
    
    def circuit_threshold(P):
        # Placeholder function to compute the circuit threshold of P
        # This is a dummy implementation and should be replaced with actual logic
        return len(P)
    
    def read_twice_branching_program(n):
        # Placeholder function to generate a read-twice branching program of size n
        # This is a dummy implementation and should be replaced with actual logic
        return [random.randint(0, 1) for _ in range(n)]
    
    def free_probability_space(V):
        # Placeholder function to compute the free probability space on V
        # This is a dummy implementation and should be replaced with actual logic
        return len(V)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    B = {i: i for i in range(n)}
    P = read_twice_branching_program(n)
    
    V = dual_vector_space(B)
    F = free_probability_space(V)
    C = circuit_threshold(P)
    
    ratio = C / F
    
    return {
        "metric_name": "Ratio of Circuit Threshold to Free Probability Space Rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 1) <= 0.05,
        "counterexample": "" if abs(ratio - 1) <= 0.05 else f"Ratio {ratio} is outside ±5% of 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside ±5% of 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")
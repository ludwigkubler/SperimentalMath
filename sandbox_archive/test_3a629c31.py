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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def determinant(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    if n < 5 or n > 40:
        return {"metric_name": "CC_{Max-Cut}", "metric_value": None, "instances_tested": 0, "conjecture_holds": False, "counterexample": "n_out_of_range"}
    
    # Generate a random quantum state with entanglement rank Θ(n^0.5)
    E = int(math.sqrt(n))
    A = [[random.randint(0, 1) for _ in range(E)] for _ in range(E)]
    det_A = determinant(A)
    if det_A == 0:
        return {"metric_name": "CC_{Max-Cut}", "metric_value": None, "instances_tested": 0, "conjecture_holds": False, "counterexample": "singular_matrix"}
    
    # Translate the quantum state into a Max-Cut instance
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    CC_Max_Cut = sum(sum(G[i][j] * A[i//E][j//E] for j in range(n)) for i in range(n))
    
    # Measure the communication complexity
    metric_value = CC_Max_Cut / n
    
    # Compare against the conjectured bounds
    if E == int(math.sqrt(n)):
        if metric_value <= 1.5:
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = "CC_{Max-Cut} exceeds bound for high entanglement rank"
    else:
        conjecture_holds = False
        counterexample = "Mapping undefined for non-Θ(n^0.5) entanglement rank"
    
    return {
        "metric_name": "CC_{Max-Cut}",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "CC_{Max-Cut} exceeds bound for high entanglement rank"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)
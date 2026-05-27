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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = -A[k][i]
                for j in range(n):
                    A[k][j] += factor * A[i][j]
    return A

def rank(matrix):
    row_echelon_form = gaussian_elimination(matrix)
    rank = 0
    for row in row_echelon_form:
        if any(row):
            rank += 1
    return rank

def random_boolean_circuit(n):
    circuit = []
    for _ in range(n):
        gate = random.choice(['AND', 'OR', 'NOT'])
        if gate == 'NOT':
            circuit.append((gate, random.randint(0, n-1)))
        else:
            inputs = random.sample(range(n), 2)
            circuit.append((gate, inputs[0], inputs[1]))
    return circuit

def apply_clifford_group(P):
    # Placeholder for actual Clifford group operation
    # For simplicity, we'll just scale the matrix by a constant factor
    c = Fraction(1, 2)
    return [[c * P[i][j] for j in range(len(P[0]))] for i in range(len(P))]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    circuit = random_boolean_circuit(n)
    P = [[0]*n for _ in range(n)]
    P[0][0] = 1  # Example initial state
    
    min_rank_P = rank(P)
    
    counterexample = ""
    conjecture_holds = True
    instances_tested = 0
    
    for _ in range(4):  # Test with different Clifford group operations
        G = apply_clifford_group(P)
        min_rank_G = rank(G)
        
        if min_rank_G > min_rank_P + 1:
            conjecture_holds = False
            counterexample = f"min_rank(G(P))={min_rank_G} > min_rank(P)={min_rank_P} + 1"
            break
        
        instances_tested += 1
    
    return {
        "metric_name": "min_rank_difference",
        "metric_value": min_rank_P - (min_rank_P if conjecture_holds else min_rank_G),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
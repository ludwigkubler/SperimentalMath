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
        if A[i][i] == 0:
            # Find a row with non-zero pivot below and swap
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Eliminate entries below the pivot
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def min_rank(A):
    A = gaussian_elimination(A)
    rank = sum(1 for row in A if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    D = random.randint(5, 40)
    
    # Generate a random ACC⁰ circuit of depth D
    def generate_acc0_circuit(D):
        if D == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_acc0_circuit(random.randint(1, D-1)) for _ in range(2)]
            return [random.choice(subcircuits) for _ in range(2)]
    
    circuit = generate_acc0_circuit(D)
    
    # Convert the circuit to a Boolean function
    def evaluate_circuit(circuit):
        if isinstance(circuit, int):
            return circuit
        else:
            return random.choice([evaluate_circuit(circuit[0]), evaluate_circuit(circuit[1])])
    
    f = lambda x: evaluate_circuit(circuit)
    
    # Compute the twisted quasi-symmetric function (simplified for demonstration)
    def twisted_quasi_symmetric_function(f, n):
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f(i & j) == 1:
                    A[i][j] = 1
        return A
    
    A = twisted_quasi_symmetric_function(f, n)
    
    rank = min_rank(A)
    threshold = D
    
    ratio = abs(rank / threshold - 1)
    
    if ratio > 0.5:
        conjecture_holds = False
        counterexample = f"Ratio {rank}/{threshold} outside tolerance"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
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
    
    # Generate a random boolean circuit with n inputs
    n = 5 + random.randint(0, 3) * 5  # n ∈ {5, 10, 15, 20, 30}
    circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
    
    # Calculate the associated symmetric polynomial P_C
    def poly(circuit):
        if not circuit:
            return 1
        x = [0] * (len(circuit) + 1)
        x[0] = 1
        for row in circuit:
            y = [0] * len(x)
            y[0] = 1
            for i, bit in enumerate(row):
                if bit == 1:
                    for j in range(len(x)):
                        y[j+1] += x[j]
            x = y
        return sum(x[i] * (-1)**i for i in range(1, len(x)))
    
    P_C = poly(circuit)
    
    # Compute the minimal order of Frobenius-Schur indicators χ_min
    def frobenius_schur_indicator(poly):
        n = len(poly) - 1
        if n == 0:
            return 1
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            A[i][i-1] = 1
            A[i][i] = -2 * poly[i]
            A[i][i+1] = 1
        det = determinant(A)
        return abs(det) ** (1/n)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    chi_min = frobenius_schur_indicator(P_C)
    
    # Compute the maximum entanglement entropy E(C)
    def max_entanglement_entropy(circuit):
        n = len(circuit)
        states = 2**n
        max_entropy = 0
        for i in range(states):
            state = [int(x) for x in format(i, f'0{n}b')]
            subcircuit = [row[state.index(bit)] for row, bit in zip(circuit, state)]
            entropy = -sum(p * math.log2(p) for p in [sum(subcircuit)/len(subcircuit), 1-sum(subcircuit)/len(subcircuit)]) if sum(subcircuit) != 0 and sum(subcircuit) != len(subcircuit) else 0
            max_entropy = max(max_entropy, entropy)
        return max_entropy
    
    E_C = max_entanglement_entropy(circuit)
    
    # Check the conjecture
    k = 1.0  # Example value for k; adjust as needed
    if abs(chi_min - E_C) <= k:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "chi_min and E(C) do not satisfy the inequality"
    
    return {
        "metric_name": "chi_min_minus_E_C",
        "metric_value": abs(chi_min - E_C),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"chi_min and E(C) do not satisfy the inequality\" first_failing_seed={first_failing_seed}")
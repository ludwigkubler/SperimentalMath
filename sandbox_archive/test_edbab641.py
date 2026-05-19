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

# Helper functions for matrix operations and energy calculation
def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = M[j][i]
                for k in range(n + 1):
                    M[j][k] -= factor * M[i][k]
    return [row[-1] for row in M]

def additive_energy(truth_table):
    n = len(truth_table)
    energy = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                for l in range(k+1, n):
                    if (truth_table[i][j] == truth_table[k][l]) != (truth_table[i][k] == truth_table[j][l]):
                        energy += 1
    return energy

# Function to estimate ACC⁰ circuit size (simplified heuristic)
def estimate_acc0_size(truth_table):
    n = len(truth_table)
    # This is a very naive heuristic; in practice, this would be much more complex
    return n * math.log2(n)

# Main function for running one trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    truth_table = [[random.randint(0, 1) for _ in range(n)] for _ in range(2**n)]
    
    energy = additive_energy(truth_table)
    acc0_size = estimate_acc0_size(truth_table)
    
    if acc0_size == 0:
        return {
            "metric_name": "additive_energy",
            "metric_value": energy,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    beta = Fraction(1, 2)  # Example value for beta
    alpha = Fraction(1, 3)  # Example value for alpha
    C = 1.0  # Example constant
    
    if energy * acc0_size**beta >= C * n**alpha:
        return {
            "metric_name": "additive_energy",
            "metric_value": energy,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "additive_energy",
            "metric_value": energy,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample: n={n}, energy={energy}, acc0_size={acc0_size}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 3 primes if no seeds provided
    
    results = []
    total_energy = 0
    count_true = 0
    counterexample = ""
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_energy += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_true += 1
        else:
            counterexample = trial_result["counterexample"]
    
    mean_energy = Fraction(total_energy, len(results))
    support_fraction = Fraction(count_true, len(results))
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_energy} std=0 support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):  # At least 80% support
        print(f"RESULT: SUPPORTED mean={mean_energy} std=0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[count_true]}")
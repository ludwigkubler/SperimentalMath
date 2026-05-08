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

def matrix_multiply(A, B):
    return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]

def matrix_add(A, B):
    return [[a + b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

def frobenius_norm(M):
    return math.sqrt(sum(x * x for row in M for x in row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define the parameters
    S = 8
    m = 8
    
    # Generate a read-twice BP
    A = [[[random.choice([0, 1]) for _ in range(S)] for _ in range(S)] for _ in range(m)]
    B = [[[random.choice([0, 1]) for _ in range(S)] for _ in range(S)] for _ in range(m)]
    
    # Compute the variable-symmetrized second-read commutator C_i
    C = [matrix_add(matrix_multiply(A[i], B[i]), matrix_multiply(B[i], A[i])) for i in range(m)]
    
    # Compute the invariant ρ(P)
    rho_P = math.log2(1 + max(frobenius_norm(C_i) ** 2 for C_i in C))
    
    # Check if the conjecture holds
    alpha = 4
    if rho_P > alpha * math.log2(S):
        return {
            "metric_name": "rho(P)",
            "metric_value": rho_P,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rho(P) = {rho_P} exceeds alpha * log2(S) = {alpha * math.log2(S)}"
        }
    
    # Check the lower bound for IP_2
    n = m // 2
    if rho_P < n / 4:
        return {
            "metric_name": "rho(P)",
            "metric_value": rho_P,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rho(P) = {rho_P} is less than n/4 = {n / 4}"
        }
    
    return {
        "metric_name": "rho(P)",
        "metric_value": rho_P,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    total_rho = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    num_supporting = sum(1 for r in results if r["conjecture_holds"])
    mean_rho = total_rho / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = num_supporting / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" in r for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} (only {num_supporting}/{len(results)} seeds supported)")
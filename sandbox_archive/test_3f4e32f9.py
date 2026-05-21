# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def fourier_hat(f, U):
    n = len(U)
    return sum(f(x) * (-1)**sum(1 for i in range(n) if x & (1 << i)) / 2**n for x in range(2**n))

def gram_matrix(f, d):
    B_d = list(combinations(range(len(f)), d))
    Q_d = [[0] * len(B_d) for _ in range(len(B_d))]
    for S, T in combinations(B_d, 2):
        Q_d[B_d.index(S)][B_d.index(T)] = fourier_hat(f, S ^ T)
        Q_d[B_d.index(T)][B_d.index(S)] = Q_d[B_d.index(S)][B_d.index(T)]
    Q_d[B_d.index(B_d[0])][B_d.index(B_d[0])] = sum(fourier_hat(f, U)**2 for U in B_d) / len(B_d)
    return Q_d

def eigenvalues(Q_d):
    n = len(Q_d)
    if n == 1:
        return [Q_d[0][0]]
    
    # Gaussian elimination to find the eigenvalues
    A = [[Q_d[i][j] for j in range(n)] for i in range(n)]
    for k in range(n):
        max_row = max(range(k, n), key=lambda i: abs(A[i][k]))
        A[k], A[max_row] = A[max_row], A[k]
        for j in range(k + 1, n):
            factor = A[j][k] / A[k][k]
            for m in range(n):
                A[j][m] -= factor * A[k][m]
    
    # Extract the eigenvalues from the diagonal
    return [A[i][i] for i in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10]
    results = []
    
    for n in n_values:
        f = lambda x: (-1)**sum(1 for i in range(n) if x & (1 << i))
        S_n = set(range(n))
        
        Q_2_S_n = gram_matrix(f, 2)
        NG_2_S_n = -min(eigenvalues(Q_2_S_n))
        
        max_NG_2_circuit = 0
        for _ in range(30):
            circuit = [random.choice(['AND', 'OR', 'MOD3']) for _ in range(n)]
            NG_2_circuit = -min(eigenvalues(gram_matrix(circuit, 2)))
            if NG_2_circuit > max_NG_2_circuit:
                max_NG_2_circuit = NG_2_circuit
        
        results.append({
            "metric_name": "NG_2",
            "metric_value": NG_2_S_n,
            "instances_tested": 1,
            "conjecture_holds": NG_2_S_n >= Fraction(1, 8 * n) and NG_2_S_n - max_NG_2_circuit >= Fraction(1, 8 * n),
            "counterexample": "" if NG_2_S_n >= Fraction(1, 8 * n) and NG_2_S_n - max_NG_2_circuit >= Fraction(1, 8 * n) else f"NG_2(S_n) = {NG_2_S_n}, max NG_2(circuit) = {max_NG_2_circuit}"
        })
    
    return {
        "seed": seed,
        "metric_name": "NG_2",
        "metric_value": sum(result["metric_value"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else next(result["counterexample"] for result in results)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")
    
    NG_2_values = [result["metric_value"] for result in run_trial(seeds[0])["instances"]]
    support_fraction = sum(result["conjecture_holds"] for result in run_trial(seeds[0])["instances"]) / len(run_trial(seeds[0])["instances"])
    
    if all(result["conjecture_holds"] for result in run_trial(seeds[0])["instances"]):
        print(f"RESULT: SUPPORTED mean={sum(NG_2_values)/len(NG_2_values):.6f} std={(sum((x - sum(NG_2_values)/len(NG_2_values))**2 for x in NG_2_values) / len(NG_2_values))**0.5:.6f} support_fraction={support_fraction:.6f}")
    elif any(not result["conjecture_holds"] for result in run_trial(seeds[0])["instances"]):
        first_failing_seed = next(seed for seed, result in enumerate(run_trial(seeds[0])["instances"], start=1) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"NG_2(S_n) < 1/(8n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
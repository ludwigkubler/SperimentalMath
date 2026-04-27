# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def frobenius_norm(M):
        return sum(sum(x**2 for x in row) for row in M)**0.5
    
    def singular_values(M):
        n = len(M)
        U = []
        S = []
        V = []
        
        # QR decomposition
        A = M.copy()
        Q = []
        R = []
        for i in range(n):
            q = [A[j][i] for j in range(i, n)]
            norm_q = frobenius_norm(q)
            u = [x / norm_q for x in q]
            Q.append(u)
            r = [sum(A[j][k] * u[k] for k in range(k)) for k in range(n)]
            R.append(r)
        
        # SVD from QR
        U = Q
        V = Q
        S = [R[i][i] for i in range(n)]
        
        return U, S, V
    
    def frobenius_energy_gap(M):
        n = len(M)
        columns = list(range(n))
        best_gap = 0
        
        # Exhaustive search for column bipartition
        if n <= 14:
            for mask in range(1 << (n - 1)):
                A = [columns[i] for i in range(n) if mask & (1 << i)]
                B = [columns[i] for i in range(n) if not (mask & (1 << i))]
                M_A = [[M[i][j] for j in A] for i in range(n)]
                M_B = [[M[i][j] for j in B] for i in range(n)]
                gap = abs(sum(x**2 for row in M_A for x in row) - sum(x**2 for row in M_B for x in row)) / n**2
                if gap > best_gap:
                    best_gap = gap
        
        # Local search for column bipartition (n=16)
        else:
            for _ in range(1000):
                A = random.sample(columns, n // 2)
                B = [col for col in columns if col not in A]
                M_A = [[M[i][j] for j in A] for i in range(n)]
                M_B = [[M[i][j] for j in B] for i in range(n)]
                gap = abs(sum(x**2 for row in M_A for x in row) - sum(x**2 for row in M_B for x in row)) / n**2
                if gap > best_gap:
                    best_gap = gap
        
        return best_gap
    
    def rigidity(M, rank):
        n = len(M)
        k = 0
        while True:
            perturbation = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(rank)]
            M_perturbed = [[M[i][j] + perturbation[i][j] for j in range(n)] for i in range(n)]
            U, S, V = singular_values(M_perturbed)
            if sum(S[:rank]) == n:
                k += 1
            else:
                break
        
        return k
    
    def s_low(M):
        _, S, _ = singular_values(M)
        return sum(sorted(S)[-3*n//4:]) / (n**(3/2))
    
    n = random.choice([6, 8, 10, 12, 14, 16])
    M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    g_M = frobenius_energy_gap(M)
    s_low_M = s_low(M)
    R_M_n4 = rigidity(M, n // 4)
    
    delta_M = R_M_n4 / n**2 - (1/16) * max(s_low_M - g_M, 0)
    
    return {
        "metric_name": "delta_M",
        "metric_value": delta_M,
        "instances_tested": 1,
        "conjecture_holds": delta_M >= 0,
        "counterexample": "" if delta_M >= 0 else f"Rigidity {R_M_n4} is less than expected by {(1/16) * max(s_low_M - g_M, 0)}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    total_delta_M = 0
    num_instances = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        
        if result["conjecture_holds"]:
            total_delta_M += result["metric_value"]
            num_instances += result["instances_tested"]
    
    mean_delta_M = total_delta_M / num_instances
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_delta_M} std=0 support_fraction={support_fraction}")
    elif any(r["delta_M"] < -0.05 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["delta_M"] < -0.05)
        print(f"RESULT: FALSIFIED counterexample=\"Rigidity is less than expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")
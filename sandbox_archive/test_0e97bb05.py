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
    
    def generate_bp(n, w):
        layers = [[] for _ in range(2)]
        for i in range(n):
            layers[0].append(random.randint(0, 1))
            layers[1].append(random.randint(0, 1))
        return layers
    
    def compute_matrix(layers, n):
        M = [[0] * (1 << (n // 2)) for _ in range(1 << (n // 2))]
        for x in range(1 << n):
            x_bits = [int(b) for b in format(x, f'0{n}b')]
            y_bits = [x_bits[i] ^ layers[0][i // 2] for i in range(n)]
            y = int(''.join(str(bit) for bit in y_bits), 2)
            M[x >> (n // 2)][y >> (n // 2)] = (-1) ** (sum(x_bits[:n // 2]) % 2)
        return M
    
    def nuclear_norm(M):
        U, _, Vt = svd(M)
        return sum(abs(s) for s in U[0])
    
    def svd(A):
        m, n = len(A), len(A[0])
        Q, R = gram_schmidt(A)
        S = [[A[i][j] if i == j else 0 for j in range(n)] for i in range(m)]
        return Q, S, R
    
    def gram_schmidt(A):
        m, n = len(A), len(A[0])
        Q = []
        R = [[0] * n for _ in range(m)]
        for j in range(n):
            v = [A[i][j] for i in range(m)]
            for i in range(j):
                r_ij = sum(Q[i][k] * A[k][j] for k in range(n))
                R[i][j] = r_ij
                v = [v[k] - r_ij * Q[i][k] for k in range(m)]
            norm_v = math.sqrt(sum(v[k]**2 for k in range(m)))
            if norm_v == 0:
                raise ValueError("Matrix is not full rank")
            R[j][j] = norm_v
            Q.append([v[k] / norm_v for k in range(m)])
        return Q, R
    
    n_values = [8, 10, 12, 14, 16]
    w_values = [2, 3, 4]
    results = []
    
    for n in n_values:
        for w in w_values:
            s = (1 << n) * w
            layers = generate_bp(n, w)
            M = compute_matrix(layers, n)
            rho = math.log2(nuclear_norm(M) / (1 << (n // 2)))
            results.append({
                "n": n,
                "w": w,
                "s": s,
                "rho": rho
            })
    
    # Check IP_2 trivial case
    IP_2_trivial = [[(-1)**(i & j) for i in range(1 << 8)] for j in range(1 << 8)]
    rho_IP_2 = math.log2(nuclear_norm(IP_2_trivial) / (1 << 4))
    
    return {
        "metric_name": "rho",
        "metric_value": sum(result["rho"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["rho"] <= 4 * math.log2(result["s"] + 1) + 1 for result in results) and rho_IP_2 >= n_values[-1] / 4 - 0.5,
        "counterexample": "" if all(result["rho"] <= 4 * math.log2(result["s"] + 1) + 1 for result in results) else f"IP_2 trivial case failed with rho={rho_IP_2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and (1 - support_fraction) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"IP_2 trivial case failed\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
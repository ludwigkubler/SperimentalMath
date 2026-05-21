# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gram_schmidt(A):
        m, n = len(A), len(A[0])
        Q = [[0] * n for _ in range(m)]
        R = [[0] * n for _ in range(n)]
        
        for j in range(n):
            v = A[j]
            for i in range(j):
                r_ij = sum(Q[i][k] * v[k] for k in range(n))
                R[i][j] = r_ij
                v = [v[k] - r_ij * Q[i][k] for k in range(n)]
            r_jj = math.sqrt(sum(v[k]**2 for k in range(n)))
            R[j][j] = r_jj
            Q[j] = [v[k] / r_jj for k in range(n)]
        
        return Q, R
    
    def svd(M):
        m, n = len(M), len(M[0])
        U, _, Vt = gram_schmidt(M)
        S = [[M[i][i] if i < min(m, n) else 0 for i in range(n)] for j in range(m)]
        return U, S, Vt
    
    def nuclear_norm(M):
        U, S, Vt = svd(M)
        return sum(abs(s) for s in sum(S, []))
    
    def generate_read_twice_bp(n, w):
        layers = [[] for _ in range(2)]
        for i in range(n):
            layer1 = random.sample(range(w), 2)
            layer2 = random.sample(range(w), 2)
            if layer1[0] != layer2[0]:
                layers[0].append((i, layer1))
                layers[1].append((i, layer2))
        return layers
    
    def compute_truth_table(bp):
        n = len(bp[0])
        truth_table = [[0] * (1 << n) for _ in range(1 << n)]
        for i in range(n):
            x = [0] * n
            y = [0] * n
            for j, layer in enumerate(bp[j]):
                if layer[0] == i:
                    x[layer[1]] = 1
                else:
                    y[layer[1]] = 1
            truth_table[x[0]][y[0]] = (-1) ** (sum(x) % 2)
        return truth_table
    
    def reshape_truth_table(truth_table, n):
        m = 1 << (n // 2)
        M = [[truth_table[i][j] for j in range(m)] for i in range(m)]
        return M
    
    n_values = [8, 10, 12, 14, 16]
    widths = [2, 3, 4]
    
    results = []
    for n in n_values:
        for w in widths:
            s = 2 ** (n // 2)
            bp = generate_read_twice_bp(n, w)
            truth_table = compute_truth_table(bp)
            M = reshape_truth_table(truth_table, n)
            rho_P = math.log2(nuclear_norm(M) / (1 << (n // 2)))
            
            results.append({
                "metric_name": "rho",
                "metric_value": rho_P,
                "instances_tested": 1,
                "conjecture_holds": rho_P <= 4 * math.log2(s + 1) + 1,
                "counterexample": "" if rho_P <= 4 * math.log2(s + 1) + 1 else f"rho(P)={rho_P} > 4*log2({s+1})+1"
            })
    
    IP_2_trivial = [[(-1)**(i & j) for j in range(1 << n)] for i in range(1 << n)]
    rho_IP_2 = math.log2(nuclear_norm(IP_2_trivial) / (1 << 4))
    
    all_rho_P = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    return {
        "seed": seed,
        "all_rho_P": all_rho_P,
        "rho_IP_2": rho_IP_2,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        results.append(result)
    
    all_rho_P = [r["all_rho_P"] for r in results]
    rho_IP_2s = [r["rho_IP_2"] for r in results]
    support_fractions = [r["support_fraction"] for r in results]
    
    mean_rho_P = sum(sum(rho) / len(rho) for rho in all_rho_P) / len(all_rho_P)
    std_rho_P = math.sqrt(sum(sum((rho[i] - mean_rho_P)**2 for i in range(len(rho))) / len(rho) for rho in all_rho_P) / len(all_rho_P))
    
    if all(s >= 0.8 for s in support_fractions):
        print(f"RESULT: SUPPORTED mean={mean_rho_P:.4f} std={std_rho_P:.4f} support_fraction={sum(support_fractions)/len(support_fractions):.2f}")
    elif any(rho_IP_2 < n / 4 - 0.5 for rho_IP_2, n in zip(rho_IP_2s, [8, 10, 12, 14, 16])):
        first_failing_seed = seeds[rho_IP_2s.index(min(rho_IP_2 for rho_IP_2 in rho_IP_2s if rho_IP_2 < n / 4 - 0.5))]
        print(f"RESULT: FALSIFIED counterexample=\"rho(IP_2_trivial) < n/4-0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
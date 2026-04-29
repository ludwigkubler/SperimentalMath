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

# Constants
N_MAX = 40
SEEDS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3  # Default seeds if none provided

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def OR(x):
        return max(x)
    
    def GadgetComposition(G1, G2):
        n1, m1 = len(G1), len(G1[0])
        n2, m2 = len(G2), len(G2[0])
        result = [[0] * (m1 * m2) for _ in range(n1 * n2)]
        for i in range(n1):
            for j in range(m1):
                for k in range(n2):
                    for l in range(m2):
                        if G1[i][j] == 1 and G2[k][l] == 1:
                            result[i*n2+k][j*m2+l] = 1
        return result
    
    def lift_function(f, G):
        n = len(G)
        lifted_G = [[0] * (n**2) for _ in range(n**2)]
        for i in range(n):
            for j in range(n):
                lifted_G[i*n+j][i*n:(i+1)*n] = [f(G[i][j])]
                lifted_G[i*n+j][(i+1)*n:] = [0] * (n*(n-1))
        return lifted_G
    
    def ProtocolPullback(Π, G):
        n = len(G)
        pullback = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if Π[i][j] == 1:
                    pullback[i][j] = 1
        return pullback
    
    def CoarsePullback(pullback, G):
        n = len(G)
        coarse_pullback = [[0] * (n//2) for _ in range(n//2)]
        for i in range(0, n, 2):
            for j in range(0, n, 2):
                if pullback[i][j] == 1 or pullback[i+1][j] == 1 or pullback[i][j+1] == 1 or pullback[i+1][j+1] == 1:
                    coarse_pullback[i//2][j//2] = 1
        return coarse_pullback
    
    def asdim(G):
        n = len(G)
        m = len(G[0])
        if n == 1 and m == 1:
            return 0
        for d in range(1, min(n, m)):
            found = False
            for i in range(d, n, d):
                for j in range(d, m, d):
                    if all(G[x][y] == G[x+d-1][y+d-1] for x in range(i-d+1, i) for y in range(j-d+1, j)):
                        found = True
                        break
                if found:
                    break
            if not found:
                return d - 1
        return min(n, m) - 1
    
    G = [[0, 1], [1, 0]]  # Base gadget: 2-bit equality
    n_values = [5, 10, 15, 20, 30, 40]
    
    results = []
    for k in range(1, N_MAX + 1):
        G_k = G
        for _ in range(k-1):
            G_k = GadgetComposition(G_k, G)
        
        for n in n_values:
            lifted_G = lift_function(OR, G_k)
            f = OR
            lifted_function = lambda x: [f(G_k[x[i]]) for i in range(n)]
            
            # Generate all deterministic protocols of cost c <= 5
            protocols = []
            for c in range(6):
                for protocol in product([0, 1], repeat=n*n):
                    if sum(protocol) == c:
                        protocols.append(protocol)
            
            for Π in protocols:
                pullback = ProtocolPullback(Π, lifted_G)
                coarse_pullback = CoarsePullback(pullback, G_k)
                m_Π = sum(sum(row) for row in coarse_pullback)
                
                if m_Π < math.log2(k+1):
                    return {
                        "metric_name": "Multiplicity",
                        "metric_value": m_Π,
                        "instances_tested": len(protocols),
                        "conjecture_holds": False,
                        "counterexample": f"Protocol Π with cost {sum(Π)} failed for k={k}, n={n}"
                    }
    
    return {
        "metric_name": "Multiplicity",
        "metric_value": sum(sum(row) for row in coarse_pullback),
        "instances_tested": len(protocols),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else SEEDS
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity did not grow logarithmically\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")
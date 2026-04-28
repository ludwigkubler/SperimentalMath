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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mult(A, B):
    m, n, p = len(A), len(B[0]), len(B)
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n+1):
                M[j][k] -= factor * M[i][k]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = (M[i][-1] - sum(M[i][j]*x[j] for j in range(i+1, n))) / M[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def hamming_distance(u, v):
        return sum(1 for a, b in zip(u, v) if a != b)
    
    def isometry_check(phi, d1, d2):
        n = len(phi)
        for u in range(n):
            for v in range(n):
                if abs(d2[phi[u][0], phi[v][0]] - d1[u, v]) > 1:
                    return False
        return True
    
    def communication_complexity(f, G, n):
        X, Y, g, d = G
        m = len(X)
        M = [[0]*m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                u = (i, j)
                v = (g(u[0], u[1]), g(v[0], v[1]))
                M[i][j] = d[u[0], v[0]] + d[u[1], v[1]]
        T = [[0]*m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                T[i][j] = f(X[i], Y[j])
        dp = [[math.inf]*m for _ in range(m)]
        dp[0][0] = 0
        for k in range(1, m**2 + 1):
            i, j = divmod(k-1, m)
            for x in range(i+1):
                for y in range(j+1):
                    if T[x][y] == T[i][j]:
                        dp[i][j] = min(dp[i][j], dp[x][y] + M[i-x][j-y])
        return dp[m-1][m-1]
    
    def asdim_certify(G, R):
        X, Y, g, d = G
        m = len(X)
        M = [[0]*m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                u = (i, j)
                v = (g(u[0], u[1]), g(v[0], v[1]))
                M[i][j] = d[u[0], v[0]] + d[u[1], v[1]]
        dp = [[math.inf]*m for _ in range(m)]
        dp[0][0] = 0
        for k in range(1, m**2 + 1):
            i, j = divmod(k-1, m)
            for x in range(i+1):
                for y in range(j+1):
                    if M[x][y] <= R:
                        dp[i][j] = min(dp[i][j], dp[x][y] + 1)
        return sum(1 for i in range(m) for j in range(m) if dp[i][j] < math.inf)
    
    n_values = [2, 3]
    K_values = [0, 1]
    c = 4
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(30):
            X = ['0']*2 + ['1']*2
            Y = ['0']*n + ['1']*n
            d1 = {(i, j): hamming_distance(X[i], Y[j]) for i in range(len(X)) for j in range(len(Y))}
            g = lambda u, v: (u[0] ^ v[0], u[1] ^ v[1])
            G1 = (X, Y, g, d1)
            
            if K_values[0] == 0:
                phi = list(itertools.permutations(range(len(X)*len(Y))))
            else:
                phi = [(i, j) for i in range(len(X)) for j in range(len(Y))]
                random.shuffle(phi)
                phi = phi[:len(phi)//2]
            
            for phi in phi:
                if K_values[0] == 1 and not isometry_check(phi, d1, d1):
                    continue
                G2 = (X, Y, lambda u, v: g(phi[u][0], phi[v][0]), d1)
                
                CC1 = communication_complexity(lambda x, y: int(x != y), G1, n)
                CC2 = communication_complexity(lambda x, y: int(x != y), G2, n)
                
                if K_values[0] == 0 and CC1 != CC2:
                    conjecture_holds = False
                    counterexample = f"K=0 isometry relabeling produced different CC"
                    break
                
                if K_values[0] == 1 and abs(CC1 - CC2) > c * n:
                    conjecture_holds = False
                    counterexample = f"K=1 perturbation produced |CC_1 - CC_2| > {c}n"
                    break
                
                instances_tested += 1
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": None,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: INCONCLUSIVE not enough evidence to support or falsify the conjecture")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
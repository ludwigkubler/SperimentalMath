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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = max(range(i, m), key=lambda r: abs(augmented[r][i]))
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        for j in range(i + 1, m):
            factor = augmented[j][i] / augmented[i][i]
            for k in range(n + 1):
                augmented[j][k] -= factor * augmented[i][k]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented[i][-1] / augmented[i][i]
        for j in range(i - 1, -1, -1):
            augmented[j][-1] -= augmented[j][i] * x[i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([4, 5, 6])
    implicants = [set() for _ in range(n)]
    for _ in range(random.randint(2, 6)):
        implicant = set()
        for j in range(n):
            if random.random() < 0.5:
                implicant.add(j)
        implicants[random.choice(range(n))].update(implicant)

    def monotone_closure(f):
        closure = f.copy()
        changed = True
        while changed:
            changed = False
            for i in range(n):
                if i not in closure and all(j in closure for j in implicants[i]):
                    closure.add(i)
                    changed = True
        return closure

    Min_f = set(range(n))
    Max_f = set()
    for i in range(1 << n):
        f = monotone_closure({j for j, bit in enumerate(bin(i)[2:].zfill(n)) if bit == '1'})
        if len(f) >= 2 and len(Min_f - f) >= 2:
            Min_f = f
            Max_f = Min_f ^ set(range(n))

    def D_plus(f):
        if not f:
            return 0
        if len(f) == 1:
            return 1
        max_depth = 0
        for i in range(n):
            if i in f and all(j in f or j not in Max_f for j in implicants[i]):
                depth = D_plus(f - {i})
                max_depth = max(max_depth, depth + 1)
        return max_depth

    def NextClosure(K, x):
        closure = set()
        for y in K:
            if all(x[i] == (y[0][i], y[1][i]) for i in range(n)):
                closure.update(y[1])
        return closure

    def Hasse_diagram(K):
        H = []
        for x in K:
            closure = NextClosure(K, x)
            H.append((x, closure))
        return H

    def longest_path(H):
        n = len(H)
        dp = [0] * n
        for i in range(n):
            dp[i] = 1
            for j in range(i):
                if all(H[j][1].issubset(H[i][1]) and H[j][0][i] == (True, False) for i in range(n)):
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)

    D_f = D_plus(Min_f)
    K_f = [(Min_f, Max_f)]
    while True:
        new_closure = NextClosure(K_f, (Min_f, Max_f))
        if not new_closure:
            break
        K_f.append((Min_f, new_closure))
        Min_f = new_closure

    H_f = Hasse_diagram(K_f)
    h_K_f = longest_path(H_f)

    conjecture_holds = D_f >= math.ceil(math.log2(h_K_f))
    counterexample = "" if conjecture_holds else f"D_+(f)={D_f}, h(K_f)={h_K_f}"

    return {
        "metric_name": "KW Depth vs. Lattice Height",
        "metric_value": D_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
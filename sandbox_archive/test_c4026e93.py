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

def hamming_distance(u, v):
    return sum(x != y for x, y in zip(u, v))

def generate_adj_matrix(X, Y, d, R):
    N = len(X) * len(Y)
    A_R = [[0] * (N ** 2) for _ in range(N ** 2)]
    for i in range(N):
        for j in range(N):
            u = X[i // len(Y)] + Y[i % len(Y)]
            v = X[j // len(Y)] + Y[j % len(Y)]
            if hamming_distance(u, v) <= R:
                A_R[i * N + j][i * N + j] = 1
    return A_R

def laplacian(A):
    D = [sum(row) for row in A]
    L = [[0] * len(D) for _ in range(len(D))]
    for i in range(len(D)):
        L[i][i] = -D[i]
        for j in range(i + 1, len(D)):
            if A[i][j]:
                L[i][j] = D[j]
                L[j][i] = D[i]
    return L

def eigsh(A, k=2, sigma=0, which='LM'):
    N = len(A)
    M = [[A[i][j] - sigma * (i == j) for j in range(N)] for i in range(N)]
    eigenvalues = []
    eigenvectors = []
    for _ in range(k):
        v = [random.random() for _ in range(N)]
        v /= math.sqrt(sum(x ** 2 for x in v))
        while True:
            Av = [sum(M[i][j] * v[j] for j in range(N)) for i in range(N)]
            lambda_v = sum(Av[i] * v[i] for i in range(N))
            if abs(lambda_v) < 1e-6:
                break
            v = [Av[i] - lambda_v * v[i] for i in range(N)]
            v /= math.sqrt(sum(x ** 2 for x in v))
        eigenvalues.append(lambda_v)
        eigenvectors.append(v)
    return eigenvalues, eigenvectors

def protocol_pullback(X, Y, d, R, n):
    N = len(X) * len(Y)
    A_R = generate_adj_matrix(X, Y, d, R)
    L_R = laplacian(A_R)
    lambda_R_n, _ = eigsh(L_R, k=2, sigma=0, which='LM')
    max_degree = max(sum(row) for row in A_R)
    
    def canonical_protocol(f):
        return {x: f(x) for x in X}
    
    def alternative_protocol(f):
        protocol = {}
        for x in X:
            protocol[x] = f(x)
        return protocol
    
    def simulate_protocol(protocol, n):
        N_n = len(X) ** n
        multiplicity = 0
        max_diameter = 0
        for i in range(N_n):
            cell = [X[i // (len(Y) ** (n - 1))], Y[(i // len(Y)) % len(Y)]]
            covered = set()
            for x in X:
                if hamming_distance(x, ''.join(cell)) <= R:
                    covered.add(x)
            multiplicity = max(multiplicity, len(covered))
            max_diameter = max(max_diameter, R)
        return multiplicity, max_diameter
    
    f_values = [f"{i:0{n}b}" for i in range(2 ** n)]
    total_multiplicity = 0
    total_max_diameter = 0
    for f_value in f_values:
        f = lambda x: int(f_value[x])
        canonical_m, canonical_r = simulate_protocol(canonical_protocol(f), n)
        alternative_m, alternative_r = simulate_protocol(alternative_protocol(f), n)
        total_multiplicity += max(canonical_m, alternative_m)
        total_max_diameter += max(canonical_r, alternative_r)
    
    N_n = len(X) ** n
    lambda_R_n = abs(lambda_R_n[1])
    bound = math.ceil(lambda_R_n * N_n / (4 * max_degree))
    return {
        "metric_name": "ProtocolPullbackMultiplicity",
        "metric_value": total_multiplicity,
        "instances_tested": len(f_values),
        "conjecture_holds": total_multiplicity >= bound,
        "counterexample": "" if total_multiplicity >= bound else f"Bound: {bound}, Got: {total_multiplicity}"
    }

def run_trial(seed: int) -> dict:
    random.seed(seed)
    X_XOR = ['0', '1']
    Y_XOR = ['0', '1']
    d_XOR = hamming_distance
    R_XOR = 2
    
    X_IND = ['00', '01', '10', '11']
    Y_IND = ['0', '1']
    d_IND = hamming_distance
    R_IND = 3
    
    results = []
    for gadget, X, Y, d, R in [(X_XOR, Y_XOR, d_XOR, R_XOR), (X_IND, Y_IND, d_IND, R_IND)]:
        for n in [1, 2, 3]:
            result = protocol_pullback(X, Y, d, R, n)
            results.append(result)
    
    total_multiplicity = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    
    return {
        "seed": seed,
        "metric_name": "ProtocolPullbackMultiplicity",
        "metric_value": total_multiplicity / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))
        results.append(result)
    
    total_multiplicity = sum(r["metric_value"] * r["instances_tested"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    mean = total_multiplicity / instances_tested
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 * r["instances_tested"] for r in results) / instances_tested)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'])}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
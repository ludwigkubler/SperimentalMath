# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def matrix_mult(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_sub(A, B):
    n = len(A)
    m = len(A[0])
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = A[i][j] - B[i][j]
    return result

def matrix_frobenius_norm(A):
    norm = 0
    for row in A:
        for val in row:
            norm += val * val
    return math.sqrt(norm)

def compute_rho(bp, n):
    s = len(bp['states'])
    A = []
    for r in range(2 * n):
        T0 = [[0 for _ in range(s)] for _ in range(s)]
        T1 = [[0 for _ in range(s)] for _ in range(s)]
        for u in range(s):
            for v in range(s):
                if bp['transitions'][r][u][v] == 0:
                    T0[u][v] += 1
                elif bp['transitions'][r][u][v] == 1:
                    T1[u][v] += 1
        A_r = [[0 for _ in range(s)] for _ in range(s)]
        for u in range(s):
            for v in range(s):
                A_r[u][v] = (T0[u][v] + T1[u][v]) / 2
        A.append(A_r)

    rho_squared = 0
    for r in range(2 * n):
        for q in range(r + 1, 2 * n):
            A_rA_q = matrix_mult(A[r], A[q])
            A_qA_r = matrix_mult(A[q], A[r])
            diff = matrix_sub(A_rA_q, A_qA_r)
            norm = matrix_frobenius_norm(diff)
            rho_squared += norm * norm

    rho = math.log2(1 + rho_squared / (s * s))
    return rho

def build_canonical_bp(n):
    states = list(range(2 ** (n // 2)))
    transitions = []
    for r in range(2 * n):
        if r < n:
            transitions.append([[(u << 1) | b for b in [0, 1]] for u in states])
        else:
            transitions.append([[(u << 1) | (b << (n // 2)) for b in [0, 1]] for u in states])
    accept = [u for u in states if bin(u).count('1') % 2 == 0]
    return {'states': states, 'transitions': transitions, 'accept': accept}

def build_random_bp(n, w, seed):
    random.seed(seed)
    s = w
    states = list(range(s))
    transitions = []
    for _ in range(2 * n):
        transitions.append([[random.randint(0, 1) for _ in range(s)] for _ in range(s)])
    accept = random.sample(states, random.randint(1, s))
    return {'states': states, 'transitions': transitions, 'accept': accept}

def evaluate_bp(bp, n):
    s = len(bp['states'])
    for x in range(2 ** n):
        y = x >> (n // 2)
        x_bits = [(x >> i) & 1 for i in range(n // 2)]
        y_bits = [(y >> i) & 1 for i in range(n // 2)]
        state = 0
        for r in range(2 * n):
            if r < n:
                bit = x_bits[r]
            else:
                bit = y_bits[r - n]
            state = bp['transitions'][r][state][bit]
        if (state in bp['accept']) != ((x * y) % 2 == 0):
            return False
    return True

def run_trial(seed):
    n_values = [4, 6, 8, 10, 12]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        canonical_bp = build_canonical_bp(n)
        rho_canonical = compute_rho(canonical_bp, n)
        s = len(canonical_bp['states'])
        if rho_canonical / math.log2(s) > 6:
            conjecture_holds = False
            counterexample = f"Canonical BP for n={n} has rho/log2(s)={rho_canonical/math.log2(s)} > 6"
            break

        for w in [2, 4, 8, 16]:
            for _ in range(6):
                bp = build_random_bp(n, w, seed)
                rho = compute_rho(bp, n)
                s = len(bp['states'])
                if rho / math.log2(s) > 6:
                    conjecture_holds = False
                    counterexample = f"Random BP for n={n}, w={w} has rho/log2(s)={rho/math.log2(s)} > 6"
                    break

                if evaluate_bp(bp, n):
                    if rho / n < 1/8:
                        conjecture_holds = False
                        counterexample = f"BP computing IP_2 for n={n} has rho/n={rho/n} < 1/8"
                        break

                instances_tested += 1
                metric_values.append(rho / math.log2(s))

                if not conjecture_holds:
                    break
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if len(metric_values) == 0:
        return {
            "metric_name": "rho/log2(s)",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid BPs generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "rho/log2(s)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, {result}}}")
        results.append(result)

    metric_values = [r['metric_value'] for r in results if r['metric_value'] is not None]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_trials")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        counterexample = next(r['counterexample'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
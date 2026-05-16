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

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def frobenius_norm(a):
    return math.sqrt(sum(sum(x**2 for x in row) for row in a))

def log2(x):
    if x <= 0:
        return float('-inf')
    return math.log2(x)

def build_bp(n, width, seed):
    random.seed(seed)
    s = width
    states = list(range(s))
    transitions = [[[random.choice(states) for _ in range(2)] for _ in range(s)] for _ in range(2*n)]
    accept = set(random.sample(states, random.randint(1, s)))
    return transitions, accept

def evaluate_bp(bp, x, y):
    transitions, accept = bp
    state = 0
    for i in range(len(transitions)):
        bit = x[i//2] if i < len(x) else y[i - len(x)]
        state = transitions[i][state][bit]
    return state in accept

def is_ip2(bp, n):
    for x in itertools.product([0, 1], repeat=n//2):
        for y in itertools.product([0, 1], repeat=n//2):
            if evaluate_bp(bp, x, y) != (sum(x) % 2 == sum(y) % 2):
                return False
    return True

def compute_rho(bp, n):
    transitions, accept = bp
    s = len(transitions[0])
    A = []
    for r in range(2*n):
        T0 = [[0]*s for _ in range(s)]
        T1 = [[0]*s for _ in range(s)]
        for u in range(s):
            v0 = transitions[r][u][0]
            v1 = transitions[r][u][1]
            T0[u][v0] += 1
            T1[u][v1] += 1
        A_r = [[Fraction(T0[i][j] + T1[i][j], 2) for j in range(s)] for i in range(s)]
        A.append(A_r)

    rho_squared = 0
    for r, q in itertools.combinations(range(2*n), 2):
        A_rA_q = matrix_mult(A[r], A[q])
        A_qA_r = matrix_mult(A[q], A[r])
        diff = matrix_sub(A_rA_q, A_qA_r)
        norm = frobenius_norm(diff)
        rho_squared += norm**2

    rho_squared /= s**2
    rho = log2(1 + rho_squared)
    return rho

def run_trial(seed):
    n_values = [4, 6, 8, 10, 12]
    results = []
    for n in n_values:
        # Build canonical read-once BP for IP_2
        width = 2**(n//2)
        transitions = [[[i*2 + b for b in range(2)] for i in range(width)] for _ in range(n)]
        accept = set(range(width))
        canonical_bp = (transitions, accept)
        rho_canonical = compute_rho(canonical_bp, n)
        s_canonical = len(transitions[0])
        ratio_canonical = rho_canonical / log2(s_canonical) if s_canonical > 1 else 0

        # Build canonical interleaved-parity BP
        transitions = [[[0, 1] if i % 2 == 0 else [1, 0] for _ in range(2)] for i in range(2*n)]
        accept = {0}
        parity_bp = (transitions, accept)
        rho_parity = compute_rho(parity_bp, n)
        s_parity = len(transitions[0])
        ratio_parity = rho_parity / log2(s_parity) if s_parity > 1 else 0

        # Build random read-twice BPs
        for w in [2, 4, 8, 16]:
            for _ in range(6):
                bp = build_bp(n, w, seed)
                if not is_ip2(bp, n):
                    continue
                rho = compute_rho(bp, n)
                s = len(bp[0][0])
                ratio = rho / log2(s) if s > 1 else 0
                results.append({
                    'n': n,
                    'width': w,
                    'rho': rho,
                    's': s,
                    'ratio': ratio,
                    'is_ip2': True
                })

        # Add canonical and parity BPs to results
        results.append({
            'n': n,
            'width': s_canonical,
            'rho': rho_canonical,
            's': s_canonical,
            'ratio': ratio_canonical,
            'is_ip2': True
        })
        results.append({
            'n': n,
            'width': s_parity,
            'rho': rho_parity,
            's': s_parity,
            'ratio': ratio_parity,
            'is_ip2': True
        })

    # Analyze results
    metric_values = [r['ratio'] for r in results if r['is_ip2']]
    ip2_metric_values = [r['rho']/r['n'] for r in results if r['is_ip2']]
    instances_tested = len(results)
    conjecture_holds = all(r['ratio'] <= 6 for r in results) and all(r['rho']/r['n'] >= 1/8 for r in results if r['is_ip2'])
    counterexample = ""

    if not all(r['ratio'] <= 6 for r in results):
        counterexample = f"Found BP with ratio > 6: {next(r for r in results if r['ratio'] > 6)}"
    elif not all(r['rho']/r['n'] >= 1/8 for r in results if r['is_ip2']):
        counterexample = f"Found IP_2 BP with rho/n < 1/8: {next(r for r in results if r['is_ip2'] and r['rho']/r['n'] < 1/8)}"

    return {
        'metric_name': 'rho_ratio',
        'metric_value': sum(metric_values) / len(metric_values) if metric_values else 0,
        'instances_tested': instances_tested,
        'conjecture_holds': conjecture_holds,
        'counterexample': counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        trials.append(result)
        print(f"TRIAL: {{'seed': {seed}, {result}}}")

    metric_values = [t['metric_value'] for t in trials]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(1 for t in trials if t['conjecture_holds']) / len(trials) if trials else 0

    if all(t['conjecture_holds'] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not t['conjecture_holds'] for t in trials):
        first_failing_seed = next(t['seed'] for t in trials if not t['conjecture_holds'])
        counterexample = next(t['counterexample'] for t in trials if not t['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
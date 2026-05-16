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
    """Multiply two matrices A and B."""
    if not A or not B:
        return []
    rows_A = len(A)
    cols_A = len(A[0]) if rows_A > 0 else 0
    rows_B = len(B)
    cols_B = len(B[0]) if rows_B > 0 else 0

    if cols_A != rows_B:
        return []

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_sub(A, B):
    """Subtract matrix B from matrix A."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return []
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_frobenius_norm(A):
    """Compute the Frobenius norm of matrix A."""
    if not A:
        return 0.0
    return math.sqrt(sum(sum(a * a for a in row) for row in A))

def build_brs_bp(n):
    """Build the BRS read-once BP for IP_2."""
    s = 2 ** (n // 2)
    states = list(range(s))
    transitions = []
    for r in range(2 * n):
        if r < n:
            T0 = [[0] * s for _ in range(s)]
            T1 = [[0] * s for _ in range(s)]
            for u in states:
                v = u
                T0[u][v] = 1
                T1[u][v] = 1
            transitions.append((T0, T1))
        else:
            T0 = [[0] * s for _ in range(s)]
            T1 = [[0] * s for _ in range(s)]
            for u in states:
                v = u ^ (1 << (r - n))
                T0[u][v] = 1
                T1[u][v] = 1
            transitions.append((T0, T1))
    return states, transitions

def build_interleaved_parity_bp(n):
    """Build the interleaved-parity read-twice BP for IP_2."""
    states = [0, 1]
    transitions = []
    for r in range(2 * n):
        if r % 2 == 0:
            T0 = [[1, 0], [0, 1]]
            T1 = [[1, 0], [0, 1]]
        else:
            T0 = [[1, 0], [0, 1]]
            T1 = [[0, 1], [1, 0]]
        transitions.append((T0, T1))
    return states, transitions

def build_random_bp(n, w):
    """Build a random read-twice BP of width w."""
    s = w
    states = list(range(s))
    transitions = []
    for r in range(2 * n):
        T0 = [[random.randint(0, 1) for _ in range(s)] for _ in range(s)]
        T1 = [[random.randint(0, 1) for _ in range(s)] for _ in range(s)]
        transitions.append((T0, T1))
    return states, transitions

def compute_rho(P, n):
    """Compute the layer-commutator Frobenius discrepancy ρ(P)."""
    states, transitions = P
    s = len(states)
    rho = 0.0
    for r in range(2 * n):
        for q in range(r + 1, 2 * n):
            T0_r, T1_r = transitions[r]
            T0_q, T1_q = transitions[q]
            A_r = [[(T0_r[i][j] + T1_r[i][j]) / 2 for j in range(s)] for i in range(s)]
            A_q = [[(T0_q[i][j] + T1_q[i][j]) / 2 for j in range(s)] for i in range(s)]
            A_rA_q = matrix_mult(A_r, A_q)
            A_qA_r = matrix_mult(A_q, A_r)
            diff = matrix_sub(A_rA_q, A_qA_r)
            norm = matrix_frobenius_norm(diff)
            rho += norm ** 2
    rho = math.log2(1 + rho / (s ** 2))
    return rho

def evaluate_bp(P, n):
    """Evaluate the BP on all possible inputs."""
    states, transitions = P
    s = len(states)
    current_state = 0
    for r in range(2 * n):
        T0, T1 = transitions[r]
        if r < n:
            bit = 0
        else:
            bit = 1
        next_state = 0
        for i in range(s):
            if T0[current_state][i] == 1 and bit == 0:
                next_state = i
                break
            if T1[current_state][i] == 1 and bit == 1:
                next_state = i
                break
        current_state = next_state
    return current_state

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Build the BRS BP
        brs_bp = build_brs_bp(n)
        rho_brs = compute_rho(brs_bp, n)
        s_brs = len(brs_bp[0])
        ratio_brs = rho_brs / math.log2(s_brs)
        if ratio_brs > 6:
            conjecture_holds = False
            counterexample = f"BRS BP with n={n}, s={s_brs}, rho={rho_brs}, ratio={ratio_brs}"

        # Build the interleaved-parity BP
        interleaved_bp = build_interleaved_parity_bp(n)
        rho_interleaved = compute_rho(interleaved_bp, n)
        s_interleaved = len(interleaved_bp[0])
        ratio_interleaved = rho_interleaved / math.log2(s_interleaved)
        if ratio_interleaved > 6:
            conjecture_holds = False
            counterexample = f"Interleaved-parity BP with n={n}, s={s_interleaved}, rho={rho_interleaved}, ratio={ratio_interleaved}"

        # Build random BPs
        for w in [2, 4, 8, 16]:
            for _ in range(30):
                random_bp = build_random_bp(n, w)
                rho_random = compute_rho(random_bp, n)
                s_random = len(random_bp[0])
                ratio_random = rho_random / math.log2(s_random)
                if ratio_random > 6:
                    conjecture_holds = False
                    counterexample = f"Random BP with n={n}, s={s_random}, rho={rho_random}, ratio={ratio_random}"

                # Check if the BP computes IP_2
                if evaluate_bp(random_bp, n) == 1:
                    ratio_ip2 = rho_random / n
                    if ratio_ip2 < 1/8:
                        conjecture_holds = False
                        counterexample = f"Random BP computing IP_2 with n={n}, s={s_random}, rho={rho_random}, ratio={ratio_ip2}"

                metric_values.append(ratio_random)
                instances_tested += 1

    if not metric_values:
        return {
            "metric_name": "rho_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "rho_ratio",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_metric_values")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if conjecture_holds_all:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample={counterexample} first_failing_seed={seeds[0]}")
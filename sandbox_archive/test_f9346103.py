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
    """Subtract matrix B from matrix A."""
    if not A or not B:
        return []
    n = len(A)
    m = len(A[0])
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = A[i][j] - B[i][j]
    return result

def matrix_frobenius_norm(A):
    """Compute the Frobenius norm of matrix A."""
    if not A:
        return 0
    n = len(A)
    m = len(A[0])
    norm = 0
    for i in range(n):
        for j in range(m):
            norm += A[i][j] ** 2
    return math.sqrt(norm)

def compute_rho(bp, n):
    """Compute the layer-commutator Frobenius discrepancy ρ(P)."""
    s = len(bp['states'])
    rho = 0
    for r in range(2 * n):
        for q in range(r + 1, 2 * n):
            A_r = [[Fraction(bp['transitions'][r][u][v] + bp['transitions'][r][u][v], 2) for v in range(s)] for u in range(s)]
            A_q = [[Fraction(bp['transitions'][q][u][v] + bp['transitions'][q][u][v], 2) for v in range(s)] for u in range(s)]
            A_r_A_q = matrix_mult(A_r, A_q)
            A_q_A_r = matrix_mult(A_q, A_r)
            diff = matrix_sub(A_r_A_q, A_q_A_r)
            norm = matrix_frobenius_norm(diff)
            rho += norm ** 2
    rho = math.log2(1 + rho / (s ** 2))
    return rho

def build_canonical_bp(n):
    """Build the canonical 'x's-then-y's' read-once BP for IP_2."""
    states = list(range(2 ** (n // 2)))
    transitions = []
    for r in range(2 * n):
        if r < n:
            transitions.append([[u ^ (1 << (r % (n // 2))) if (u >> (r % (n // 2))) & 1 else u for _ in range(2 ** (n // 2))] for u in range(2 ** (n // 2))])
        else:
            transitions.append([[u ^ (1 << ((r - n) % (n // 2))) if (u >> ((r - n) % (n // 2))) & 1 else u for _ in range(2 ** (n // 2))] for u in range(2 ** (n // 2))])
    return {'states': states, 'transitions': transitions}

def build_random_bp(n, w, seed):
    """Build a random read-twice BP of width w."""
    random.seed(seed)
    states = list(range(w))
    transitions = []
    for _ in range(2 * n):
        transitions.append([[random.randint(0, 1) for _ in range(w)] for _ in range(w)])
    return {'states': states, 'transitions': transitions}

def evaluate_bp(bp, n, x, y):
    """Evaluate the BP on input (x, y)."""
    state = 0
    for r in range(2 * n):
        if r < n:
            state = bp['transitions'][r][state][x[r]]
        else:
            state = bp['transitions'][r][state][y[r - n]]
    return state

def is_ip2(bp, n):
    """Check if the BP computes IP_2."""
    for x in itertools.product([0, 1], repeat=n):
        for y in itertools.product([0, 1], repeat=n):
            if evaluate_bp(bp, n, x, y) != sum(xi * yi for xi, yi in zip(x, y)) % 2:
                return False
    return True

def run_trial(seed):
    """Run one trial with the given seed."""
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Build the canonical BP
        canonical_bp = build_canonical_bp(n)
        rho_canonical = compute_rho(canonical_bp, n)
        s = len(canonical_bp['states'])
        if rho_canonical / math.log2(s) > 6:
            conjecture_holds = False
            counterexample = f"Canonical BP with n={n} has ρ(P)/log_2(s)={rho_canonical / math.log2(s)} > 6"
            break

        # Build random BPs
        for w in [2, 4, 8, 16]:
            for _ in range(30):
                bp = build_random_bp(n, w, seed)
                rho = compute_rho(bp, n)
                s = len(bp['states'])
                if rho / math.log2(s) > 6:
                    conjecture_holds = False
                    counterexample = f"Random BP with n={n}, w={w} has ρ(P)/log_2(s)={rho / math.log2(s)} > 6"
                    break
                if is_ip2(bp, n):
                    if rho / n < 1/8:
                        conjecture_holds = False
                        counterexample = f"BP computing IP_2 with n={n} has ρ(P)/n={rho / n} < 1/8"
                        break
                instances_tested += 1
                metric_values.append(rho / math.log2(s) if not is_ip2(bp, n) else rho / n)

    if conjecture_holds:
        metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    else:
        metric_value = 0

    return {
        "metric_name": "rho_ratio",
        "metric_value": metric_value,
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
        print(f"TRIAL: {{'seed': {seed}, {result}}}")
        metric_values.append(result["metric_value"])
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]
            break

    if conjecture_holds_all:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction=1.0")
    else:
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={seeds[0]}")
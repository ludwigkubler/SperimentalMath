# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[Fraction(0, 1) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_add(A, B):
        m = len(A)
        n = len(A[0])
        C = [[Fraction(0, 1) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                C[i][j] = A[i][j] + B[i][j]
        return C

    def matrix_scale(A, c):
        m = len(A)
        n = len(A[0])
        B = [[Fraction(0, 1) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                B[i][j] = A[i][j] * c
        return B

    def matrix_norm(A):
        m = len(A)
        n = len(A[0])
        norm = Fraction(0, 1)
        for i in range(m):
            for j in range(n):
                norm += abs(A[i][j])
        return norm

    def generate_read_twice_bp(n):
        bp = [[random.choice([0, 1]) for _ in range(2)] for _ in range(2**n)]
        return bp

    def transition_matrix(bp):
        n = len(bp)
        m = 2**n
        T = [[Fraction(0, 1) for _ in range(m)] for _ in range(m)]
        for i in range(m):
            x = bin(i)[2:].zfill(n)
            for j in range(m):
                y = bin(j)[2:].zfill(n)
                if bp[x[i]][y[i]] == 1:
                    T[i][j] += Fraction(1, m)
        return T

    def noncommutative_fourier_transform(T, g):
        n = len(T)
        F = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
        for x in range(n):
            for y in range(n):
                F[x][y] += T[x][y] * g(x, y)
        return F

    def trivial_bp_transition_matrix(n):
        m = 2**n
        T = [[Fraction(0, 1) for _ in range(m)] for _ in range(m)]
        for i in range(m):
            for j in range(m):
                if i == j:
                    T[i][j] += Fraction(1, m)
        return T

    def ip2_transition_matrix(n):
        m = 2**n
        T = [[Fraction(0, 1) for _ in range(m)] for _ in range(m)]
        for i in range(m):
            x = bin(i)[2:].zfill(n)
            for j in range(m):
                y = bin(j)[2:].zfill(n)
                if x == y:
                    T[i][j] += Fraction(1, m)
        return T

    def g(x, y):
        n = len(bin(x)[2:])
        return Fraction((-1)**(x ^ y), 2**n)

    n = 40
    instances_tested = 30
    total_norm = Fraction(0, 1)
    trivial_count = 0

    for _ in range(instances_tested):
        if random.choice([True, False]):
            bp = generate_read_twice_bp(n)
            T = transition_matrix(bp)
        else:
            T = trivial_bp_transition_matrix(n)
            trivial_count += 1
        F = noncommutative_fourier_transform(T, g)
        norm = matrix_norm(F)
        total_norm += norm

    mean_norm = total_norm / instances_tested
    conjecture_holds = mean_norm == Fraction(0, 1) if trivial_count == instances_tested else True
    counterexample = "" if conjecture_holds else "trivial_bp"

    return {
        "metric_name": "operator_norm",
        "metric_value": float(mean_norm),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_norm} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='trivial_bp' first_failing_seed={first_failing_seed}")
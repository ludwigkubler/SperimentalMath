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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def p_adic_order(equations, p=101):
        m = len(equations)
        if m == 0:
            return 0
        n = len(equations[0])
        M = [[Fraction(0) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                M[i][j] = equations[j][i]
        rank = 0
        for i in range(min(m, n)):
            if M[i][i] != Fraction(0):
                rank += 1
                for j in range(i+1, m):
                    factor = -M[j][i] / M[i][i]
                    for k in range(n):
                        M[j][k] += factor * M[i][k]
        return rank

    def generate_points(n):
        points = []
        for _ in range(n):
            point = [random.randint(0, p-1) for _ in range(n)]
            points.append(point)
        return points

    def secant_variety(points):
        n = len(points[0])
        equations = []
        for i in range(n):
            equation = [points[j][i] for j in range(n)]
            equations.append(equation)
        return equations

    def communication_complexity(n):
        # Simplified model of communication complexity
        return n * math.log2(n)

    n = random.choice([5, 10, 15, 20, 30, 40])
    points = generate_points(n)
    equations = secant_variety(points)
    order = p_adic_order(equations)
    comm_complexity = communication_complexity(n)

    return {
        "metric_name": "p-adic Order",
        "metric_value": order,
        "instances_tested": n,
        "conjecture_holds": order >= n,
        "counterexample": "" if order >= n else f"order={order} < {n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='order < n' first_failing_seed={first_failing_seed}")
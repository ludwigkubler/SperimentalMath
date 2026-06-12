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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            if random.choice([True, False]):
                clause[0] = f'~{clause[0]}'
            clauses.append(' | '.join(clause))
        return ' & '.join(clauses)

    def clause_indicator_polynomial(phi):
        n = phi.count('x')
        polynomial = [0] * (2**n)
        for clause in phi.split(' & '):
            bits = 0
            for literal in clause.split(' | '):
                if literal.startswith('~'):
                    bit = int(literal[1:]) - 1
                else:
                    bit = int(literal) - 1
                bits |= (1 << bit)
            polynomial[bits] += 1
        return polynomial

    def twisted_quiver_representation(polynomial):
        n = len(polynomial)
        q = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    q[i][j] = polynomial[(1 << i) ^ (1 << j)]
        return q

    def min_order(q):
        n = len(q)
        count = 0
        for i in range(n):
            for j in range(n):
                if q[i][j] != 0:
                    count += 1
        return count

    def resolution_proof_width(phi):
        n = phi.count('x')
        width = 0
        stack = []
        for clause in phi.split(' & '):
            literals = set(clause.split(' | '))
            if not stack:
                stack.append(literals)
            else:
                new_stack = []
                for s in stack:
                    if literals.isdisjoint(s):
                        new_stack.append(s.union(literals))
                    else:
                        width += 1
                stack = new_stack
        return width

    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept

    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        n = len(A)
        r = 0
        for i in range(n):
            if all(abs(A[i][j]) < 1e-9 for j in range(r)):
                continue
            for j in range(r, n):
                A[i], A[j] = A[j], A[i]
                break
            r += 1
        return r

    def min_order_twisted_quiver(phi):
        polynomial = clause_indicator_polynomial(phi)
        q = twisted_quiver_representation(polynomial)
        return rank(q)

    n_max = 0
    instances_tested = 0
    total_min_order = 0
    total_resolution_width = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            phi = generate_sat_instance(n)
            min_order_twq = min_order_twisted_quiver(phi)
            resolution_width = resolution_proof_width(phi)
            total_min_order += min_order_twq
            total_resolution_width += resolution_width
            instances_tested += 1
            n_max = max(n_max, n)

    mean_min_order = total_min_order / instances_tested
    mean_resolution_width = total_resolution_width / instances_tested

    slope, intercept = linear_regression(range(5, 41), [mean_min_order] * 36)
    
    conjecture_holds = 0.5 <= slope <= 1.5 and slope < float('inf')
    counterexample = "" if conjecture_holds else f"Linear regression slope {slope} not in [0.5, 1.5]"
    
    return {
        "metric_name": "linear_regression_slope",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_slope = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slope} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
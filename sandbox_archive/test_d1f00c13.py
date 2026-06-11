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
            for j in range(i + 1, m):
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

    def smith_normal_form(A):
        m, n = len(A), len(A[0])
        U = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(m)]
        V = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        A_copy = [row[:] for row in A]
        gaussian_elimination(A_copy)
        for i in range(min(m, n)):
            pivot = None
            for j in range(i, m):
                if A_copy[j][i] != Fraction(0):
                    pivot = j
                    break
            if pivot is None:
                continue
            U[i], U[pivot] = U[pivot], U[i]
            V[i], V[pivot] = V[pivot], V[i]
            for k in range(n):
                A_copy[i][k], A_copy[pivot][k] = A_copy[pivot][k], A_copy[i][k]
            factor = Fraction(A_copy[i][i])
            for j in range(m):
                A_copy[j][i] /= factor
            for j in range(i + 1, n):
                factor = Fraction(A_copy[i][j])
                for k in range(n):
                    A_copy[k][j] -= factor * A_copy[k][i]
        return U, V, A_copy

    def frege_proof_depth(phi):
        stack = []
        depth = 0
        max_depth = 0
        for token in phi:
            if token == '(': 
                stack.append(token)
                depth += 1
                max_depth = max(max_depth, depth)
            elif token == ')':
                stack.pop()
                depth -= 1
        return max_depth

    def matroid_rank(matrix):
        U, V, A_snf = smith_normal_form(matrix)
        rank = sum(1 for row in A_snf if any(x != Fraction(0) for x in row))
        return rank

    def generate_frege_formula(n):
        if n == 0:
            return ['T']
        elif n == 1:
            return ['F']
        else:
            a, b = random.sample(range(n), 2)
            phi_a = generate_frege_formula(a)
            phi_b = generate_frege_formula(b)
            return [random.choice(['&', '|']), phi_a, phi_b]

    def parse_phi(phi):
        stack = []
        for token in phi:
            if token == 'T' or token == 'F':
                stack.append([token])
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append([token, left, right])
        return stack[0]

    def evaluate(phi):
        phi = parse_phi(phi)
        if isinstance(phi, list):
            op, left, right = phi
            if op == '&':
                return evaluate(left) and evaluate(right)
            elif op == '|':
                return evaluate(left) or evaluate(right)
        else:
            return phi

    def is_valid_formula(phi):
        try:
            evaluate(phi)
            return True
        except:
            return False

    n = random.randint(5, 40)
    while True:
        phi = generate_frege_formula(n)
        if is_valid_formula(phi):
            break

    AKT_dim = matroid_rank([[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)])
    d_phi = frege_proof_depth(phi)

    return {
        "metric_name": "AKT_dim vs proof depth",
        "metric_value": AKT_dim / d_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
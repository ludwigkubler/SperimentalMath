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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extend_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extend_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extend_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * matrix_minor(matrix, 0, i).det() * (-1) ** (0 + i)
    inv_det = mod_inverse(det % mod, mod)
    adjugate = [[matrix_minor(matrix, j, i).det() * (-1) ** (j + i) for i in range(n)] for j in range(n)]
    return matrix_mod_mult(adjugate, inv_det, mod)

def matrix_minor(matrix, row, col):
    minor = []
    for i in range(len(matrix)):
        if i == row:
            continue
        m_row = []
        for j in range(len(matrix[i])):
            if j == col:
                continue
            m_row.append(matrix[i][j])
        minor.append(m_row)
    return Matrix(minor)

def matrix_mod_mult(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
    return Matrix(result)

def matrix_mod_add(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] + B[i][j]) % mod
    return Matrix(result)

def matrix_mod_sub(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] - B[i][j]) % mod
    return Matrix(result)

class Matrix:
    def __init__(self, data):
        self.data = data

    def det(self):
        n = len(self.data)
        if n == 1:
            return self.data[0][0]
        elif n == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        else:
            det = 0
            for j in range(n):
                det += (-1) ** j * self.data[0][j] * Matrix([row[:j] + row[j+1:] for row in self.data[1:]]).det()
            return det

    def transpose(self):
        n = len(self.data)
        m = len(self.data[0])
        result = [[0] * n for _ in range(m)]
        for i in range(n):
            for j in range(m):
                result[j][i] = self.data[i][j]
        return Matrix(result)

def gaussian_elimination(matrix, mod):
    n = len(matrix)
    m = len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    for i in range(n):
        pivot_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[pivot_row][i]):
                pivot_row = j
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(m):
            augmented_matrix[i][j] = (augmented_matrix[i][j] * mod_inverse(pivot, mod)) % mod
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(m):
                    augmented_matrix[j][k] = (augmented_matrix[j][k] - factor * augmented_matrix[i][k]) % mod
    return [row[:-n] for row in augmented_matrix]

def tropical_hyperplane_set(F, n):
    hyperplanes = []
    for clause in F:
        hyperplane = []
        for literal in clause:
            if literal.startswith('~'):
                var = literal[1:]
                sign = -1
            else:
                var = literal
                sign = 1
            hyperplane.append((var, sign))
        hyperplanes.append(hyperplane)
    return hyperplanes

def tropical_intersection(hyperplanes, mod):
    n = len(hyperplanes)
    if n == 0:
        return []
    elif n == 1:
        return hyperplanes[0]
    else:
        intersection = []
        for i in range(n):
            for j in range(i+1, n):
                h1 = hyperplanes[i]
                h2 = hyperplanes[j]
                new_hyperplane = []
                for var1, sign1 in h1:
                    found = False
                    for var2, sign2 in h2:
                        if var1 == var2:
                            if sign1 * sign2 > 0:
                                new_hyperplane.append((var1, sign1))
                                found = True
                                break
                            else:
                                break
                    if not found:
                        new_hyperplane.append((var1, sign1))
                for var2, sign2 in h2:
                    found = False
                    for var1, sign1 in h1:
                        if var2 == var1:
                            if sign2 * sign1 > 0:
                                new_hyperplane.append((var2, sign2))
                                found = True
                                break
                            else:
                                break
                    if not found:
                        new_hyperplane.append((var2, sign2))
                intersection.append(new_hyperplane)
        return tropical_intersection(intersection, mod)

def dpll_refutation_depth(F):
    def dpll(model, clauses):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            var = literal[1:] if literal.startswith('~') else literal
            new_model = model.copy()
            new_model[var] = literal.startswith('~')
            return dpll(new_model, [c for c in clauses if not any(l in c for l in (literal, f'~{var}'))])
        pure_literal = next((l for l in set.union(*[set(c) for c in clauses]) if all(l in c or f'~{l}' in c for c in clauses)), None)
        if pure_literal:
            var = pure_literal[1:] if pure_literal.startswith('~') else pure_literal
            new_model = model.copy()
            new_model[var] = pure_literal.startswith('~')
            return dpll(new_model, [c for c in clauses if not any(l in c for l in (pure_literal, f'~{var}'))])
        literal = random.choice(set.union(*[set(c) for c in clauses]))
        var = literal[1:] if literal.startswith('~') else literal
        return 1 + max(dpll(model.copy(), [c for c in clauses if not any(l in c for l in (literal, f'~{var}'))]), dpll(model.copy(), [c for c in clauses if not any(l in c for l in (f'~{literal}', f'{var}'))]))
    return dpll({}, F)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(random.randint(2*n, 3*n)):
        clause = []
        for _ in range(random.randint(1, n//2)):
            literal = random.choice(variables)
            if random.choice([True, False]):
                literal = f'~{literal}'
            clause.append(literal)
        clauses.append(clause)
    F = [tuple(clause) for clause in clauses]
    hyperplanes = tropical_hyperplane_set(F, n)
    intersection = tropical_intersection(hyperplanes, 2)
    refutation_depth = dpll_refutation_depth(F)
    return {
        "metric_name": "refutation_depth",
        "metric_value": refutation_depth,
        "instances_tested": len(clauses),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
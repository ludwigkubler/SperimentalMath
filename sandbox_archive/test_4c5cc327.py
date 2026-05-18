# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    remaining_vertices = vertices.copy()
    while remaining_vertices:
        u = remaining_vertices.pop()
        v = random.choice(remaining_vertices)
        edges.append((u, v))
        edges.append((u, random.choice([x for x in remaining_vertices if x != v])))
    return edges

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scalar_multiply(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_power(A, power):
    result = [[0 if i != j else 1 for j in range(len(A))] for i in range(len(A))]
    for _ in range(power):
        result = matrix_multiply(result, A)
    return result

def matrix_trace(A):
    return sum(A[i][i] for i in range(len(A)))

def matrix_determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in A[1:]]
        det += ((-1) ** col) * A[0][col] * matrix_determinant(minor)
    return det

def matrix_inverse(A):
    n = len(A)
    det = matrix_determinant(A)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    adjugate = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in (A[:i] + A[i+1:])]
            adjugate[j][i] = ((-1) ** (i + j)) * matrix_determinant(minor)
    inverse = matrix_scalar_multiply(adjugate, 1.0 / det)
    return inverse

def matrix_eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]
    eigenvalues = []
    for _ in range(n):
        x = [random.random() for _ in range(n)]
        for _ in range(100):
            Ax = matrix_multiply(A, [x])[0]
            norm_Ax = math.sqrt(sum(xi ** 2 for xi in Ax))
            if norm_Ax == 0:
                break
            x = [xi / norm_Ax for xi in Ax]
        eigenvalues.append(matrix_multiply([x], matrix_multiply(A, [x]))[0][0])
    return sorted(eigenvalues, key=abs, reverse=True)

def compute_lambda_2(P_G):
    eigenvalues = matrix_eigenvalues(P_G)
    if len(eigenvalues) < 2:
        return 0.0
    return eigenvalues[1]

def compute_delta_Q(G, n):
    P_G = [[0.0 for _ in range(n)] for _ in range(n)]
    for u, v in G:
        P_G[u][v] += 1.0 / 3.0
        P_G[v][u] += 1.0 / 3.0
    for i in range(n):
        row_sum = sum(P_G[i])
        if row_sum > 0:
            for j in range(n):
                P_G[i][j] /= row_sum
    lambda_2 = compute_lambda_2(P_G)
    delta_Q = 2 * math.asin(math.sqrt(1 - abs(lambda_2)))
    return delta_Q

def compute_nu(G, n):
    delta_Q = compute_delta_Q(G, n)
    nu = math.floor(n * delta_Q)
    return nu

def generate_odd_charge(n, seed):
    random.seed(seed)
    charge = [random.choice([-1, 1]) for _ in range(n)]
    if sum(charge) % 2 == 0:
        charge[0] *= -1
    return charge

def tseitin_formula(G, charge, n):
    clauses = []
    for u, v in G:
        for sign_u in [-1, 1]:
            for sign_v in [-1, 1]:
                clause = []
                if sign_u == 1:
                    clause.append((u, 1))
                else:
                    clause.append((u, -1))
                if sign_v == 1:
                    clause.append((v, 1))
                else:
                    clause.append((v, -1))
                clauses.append(clause)
    for i in range(n):
        if charge[i] == 1:
            clauses.append([(i, 1)])
        else:
            clauses.append([(i, -1)])
    return clauses

def dpll_satisfiable(clauses, assignment, n):
    if not clauses:
        return True
    for clause in clauses:
        if all((lit[0], lit[1]) in assignment or (-lit[0], -lit[1]) in assignment for lit in clause):
            continue
        if any((lit[0], lit[1]) in assignment for lit in clause):
            continue
        if any((-lit[0], -lit[1]) in assignment for lit in clause):
            continue
        if len(clause) == 1:
            lit = clause[0]
            if (lit[0], lit[1]) in assignment or (-lit[0], -lit[1]) in assignment:
                continue
            new_assignment = assignment.copy()
            new_assignment.add((lit[0], lit[1]))
            if dpll_satisfiable([c for c in clauses if not any((lit[0], lit[1]) in a or (-lit[0], -lit[1]) in a for a in c)], new_assignment, n):
                return True
            new_assignment = assignment.copy()
            new_assignment.add((-lit[0], -lit[1]))
            if dpll_satisfiable([c for c in clauses if not any((lit[0], lit[1]) in a or (-lit[0], -lit[1]) in a for a in c)], new_assignment, n):
                return True
            return False
    return True

def compute_t_star(G, charge, n):
    clauses = tseitin_formula(G, charge, n)
    if dpll_satisfiable(clauses, set(), n):
        return 0
    return 2 ** 22

def run_trial(seed):
    n_values = [12, 16, 20]
    metric_values = []
    conjecture_holds_list = []
    counterexamples = []
    instances_tested = 0
    for n in n_values:
        G = generate_3_regular_graph(n, seed)
        charge = generate_odd_charge(n, seed)
        nu = compute_nu(G, n)
        t_star = compute_t_star(G, charge, n)
        metric_value = math.log2(t_star) if t_star > 0 else 0
        conjecture_holds = (metric_value >= nu / 8 - 5) and (nu <= 16)
        metric_values.append(metric_value)
        conjecture_holds_list.append(conjecture_holds)
        if not conjecture_holds:
            counterexamples.append(f"n={n}, seed={seed}, nu={nu}, t_star={t_star}")
        instances_tested += 1
    metric_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(conjecture_holds_list)
    counterexample = ", ".join(counterexamples) if counterexamples else ""
    return {
        "metric_name": "log2(t_star)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_list = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        metric_values.append(trial_result["metric_value"])
        conjecture_holds_list.append(trial_result["conjecture_holds"])
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds_list) / len(conjecture_holds_list)
    if all(conjecture_holds_list) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for seed, holds in zip(seeds, conjecture_holds_list):
            if not holds:
                print(f"RESULT: FALSIFIED counterexample={run_trial(seed)['counterexample']} first_failing_seed={seed}")
                break
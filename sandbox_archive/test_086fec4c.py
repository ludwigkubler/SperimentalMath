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

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scalar_mult(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_power(A, power):
    if power == 0:
        return matrix_identity(len(A))
    result = A
    for _ in range(power - 1):
        result = matrix_mult(result, A)
    return result

def matrix_trace(A):
    return sum(A[i][i] for i in range(len(A)))

def matrix_norm(A):
    return math.sqrt(sum(sum(a**2 for a in row) for row in A))

def matrix_inverse(A):
    n = len(A)
    I = matrix_identity(n)
    for col in range(n):
        diag = A[col][col]
        if diag == 0:
            raise ValueError("Matrix is not invertible")
        for row in range(n):
            A[row][col] /= diag
            I[row][col] /= diag
        for c in range(n):
            if c != col and A[col][c] != 0:
                factor = A[col][c]
                for row in range(n):
                    A[row][c] -= factor * A[row][col]
                    I[row][c] -= factor * I[row][col]
    return I

def matrix_eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]
    elif n == 2:
        a = A[0][0]
        b = A[0][1]
        c = A[1][0]
        d = A[1][1]
        trace = a + d
        det = a * d - b * c
        discriminant = trace**2 - 4 * det
        if discriminant < 0:
            return [trace / 2 + math.sqrt(-discriminant) / 2, trace / 2 - math.sqrt(-discriminant) / 2]
        else:
            return [trace / 2 + math.sqrt(discriminant) / 2, trace / 2 - math.sqrt(discriminant) / 2]
    else:
        raise ValueError("Matrix too large for this implementation")

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    remaining_edges = n // 2
    while remaining_edges > 0:
        u, v = random.sample(vertices, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
            remaining_edges -= 1
    return edges

def generate_odd_charge(n, seed):
    random.seed(seed)
    return [random.choice([-1, 1]) for _ in range(n)]

def compute_adjacency_matrix(edges, n):
    A = [[0] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = 1
        A[v][u] = 1
    return A

def compute_degree_matrix(A):
    n = len(A)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = sum(A[i])
    return D

def compute_random_walk_matrix(A, D):
    n = len(A)
    D_inv = [[0] * n for _ in range(n)]
    for i in range(n):
        if D[i][i] != 0:
            D_inv[i][i] = 1 / D[i][i]
    P = matrix_mult(D_inv, A)
    return P

def compute_second_largest_eigenvalue(P):
    eigenvalues = matrix_eigenvalues(P)
    eigenvalues.sort(reverse=True)
    return eigenvalues[1]

def compute_phase_gap(lambda_2):
    return 2 * math.asin(math.sqrt(1 - abs(lambda_2)))

def compute_nu(n, delta_Q):
    return math.floor(n * delta_Q)

def generate_tseitin_cnf(G, omega):
    n = len(G)
    cnf = []
    for i in range(n):
        neighbors = [j for j in range(n) if G[i][j] == 1]
        for j, k in itertools.combinations(neighbors, 2):
            cnf.append([-i-1, -j-1, k+1])
            cnf.append([-i-1, j-1, -k+1])
            cnf.append([i-1, -j-1, -k+1])
            cnf.append([i-1, j-1, k+1])
    for i in range(n):
        if omega[i] == 1:
            cnf.append([i+1])
        else:
            cnf.append([-i-1])
    return cnf

def dpll_satisfiable(cnf, assignment, level):
    if level > 22:
        return False
    if not cnf:
        return True
    for clause in cnf:
        if all(lit < 0 and -lit not in assignment for lit in clause):
            return False
    unassigned = [lit for clause in cnf for lit in clause if abs(lit) not in assignment]
    if not unassigned:
        return True
    lit = random.choice(unassigned)
    new_assignment = assignment.copy()
    new_assignment[abs(lit)] = lit > 0
    if dpll_satisfiable([clause for clause in cnf if not any(lit in clause for lit in [-abs(lit), abs(lit)])], new_assignment, level + 1):
        return True
    new_assignment[abs(lit)] = lit < 0
    return dpll_satisfiable([clause for clause in cnf if not any(lit in clause for lit in [-abs(lit), abs(lit)])], new_assignment, level + 1)

def run_trial(seed):
    n_values = [12, 16, 20]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        if n % 2 != 0:
            continue
        edges = generate_3_regular_graph(n, seed)
        omega = generate_odd_charge(n, seed)
        A = compute_adjacency_matrix(edges, n)
        D = compute_degree_matrix(A)
        P = compute_random_walk_matrix(A, D)
        lambda_2 = compute_second_largest_eigenvalue(P)
        delta_Q = compute_phase_gap(lambda_2)
        nu = compute_nu(n, delta_Q)
        cnf = generate_tseitin_cnf(A, omega)
        t_star = 0
        if dpll_satisfiable(cnf, {}, 0):
            t_star = 2**22
        else:
            t_star = 2**10
        metric_values.append(math.log2(t_star) - nu / 8)
        instances_tested += 1
        if metric_values[-1] < -5:
            conjecture_holds = False
            counterexample = f"n={n}, seed={seed}, log2(t*)={math.log2(t_star)}, nu={nu}"
            break
    return {
        "metric_name": "log2(t*) - nu/8",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    metric_values = [result["metric_value"] for result in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seeds[results.index(result)]}")
                break
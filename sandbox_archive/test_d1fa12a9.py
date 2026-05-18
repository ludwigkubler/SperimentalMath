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
    vertices = list(range(n))
    edges = []
    remaining_vertices = vertices.copy()
    while remaining_vertices:
        u = remaining_vertices.pop()
        if len(remaining_vertices) < 2:
            raise ValueError("Cannot generate 3-regular graph with odd n")
        neighbors = random.sample(remaining_vertices, 2)
        for v in neighbors:
            edges.append((u, v))
            remaining_vertices.remove(v)
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

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scale(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_power(A, power):
    result = matrix_identity(len(A))
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
        det += ((-1)**col) * A[0][col] * matrix_determinant(minor)
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
            adjugate[j][i] = ((-1)**(i+j)) * matrix_determinant(minor)
    return [[adjugate[i][j] / det for j in range(n)] for i in range(n)]

def matrix_eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]
    # Using the power method for the largest eigenvalue
    x = [1.0] * n
    for _ in range(100):
        x_new = matrix_multiply(A, [x])[0]
        norm = math.sqrt(sum(xi**2 for xi in x_new))
        x = [xi / norm for xi in x_new]
    lambda_max = sum(A[i][i] * x[i] for i in range(n))
    # Shift and invert for the second largest eigenvalue
    shift = 0.5 * lambda_max
    I = matrix_identity(n)
    A_shifted = matrix_subtract(A, matrix_scale(I, shift))
    A_inv = matrix_inverse(A_shifted)
    x = [1.0] * n
    for _ in range(100):
        x_new = matrix_multiply(A_inv, [x])[0]
        norm = math.sqrt(sum(xi**2 for xi in x_new))
        x = [xi / norm for xi in x_new]
    lambda_2 = sum(A[i][i] * x[i] for i in range(n)) + shift
    return [lambda_max, lambda_2]

def generate_odd_charge(n, seed):
    random.seed(seed)
    return [random.choice([-1, 1]) for _ in range(n)]

def compute_phase_gap(edges, n):
    # Build adjacency matrix
    adj = [[0] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = 1
        adj[v][u] = 1
    # Build degree matrix
    deg = [[0] * n for _ in range(n)]
    for i in range(n):
        deg[i][i] = sum(adj[i])
    # Build random walk matrix
    deg_inv = matrix_inverse(deg)
    P = matrix_multiply(deg_inv, adj)
    # Compute eigenvalues
    eigenvalues = matrix_eigenvalues(P)
    lambda_2 = max(eigenvalues[1], -eigenvalues[1])
    delta_Q = 2 * math.asin(math.sqrt(1 - lambda_2))
    nu = math.floor(n * delta_Q)
    return nu, delta_Q

def tseitin_formula(edges, charge):
    clauses = []
    for u, v in edges:
        clauses.append([(u, 1), (v, 1), (u, v, 1)])
        clauses.append([(u, -1), (v, 1), (u, v, -1)])
        clauses.append([(u, 1), (v, -1), (u, v, -1)])
        clauses.append([(u, -1), (v, -1), (u, v, 1)])
    for i, c in enumerate(charge):
        clauses.append([(i, c)])
    return clauses

def dpll_satisfiable(clauses, assignment, max_nodes=2**22):
    if max_nodes <= 0:
        return False
    max_nodes -= 1
    # Check if all clauses are satisfied
    satisfied = True
    for clause in clauses:
        clause_satisfied = False
        for literal in clause:
            if isinstance(literal, tuple):
                if len(literal) == 2:
                    var, val = literal
                    if assignment.get(var, 0) == val:
                        clause_satisfied = True
                        break
                else:
                    var1, var2, val = literal
                    if assignment.get(var1, 0) + assignment.get(var2, 0) == val:
                        clause_satisfied = True
                        break
            else:
                var, val = literal
                if assignment.get(var, 0) == val:
                    clause_satisfied = True
                    break
        if not clause_satisfied:
            satisfied = False
            break
    if satisfied:
        return True
    # Find pure literals
    pure_literals = {}
    for clause in clauses:
        for literal in clause:
            if isinstance(literal, tuple):
                if len(literal) == 2:
                    var, val = literal
                    if var in pure_literals:
                        if pure_literals[var] != val:
                            del pure_literals[var]
                    else:
                        pure_literals[var] = val
                else:
                    var1, var2, val = literal
                    if var1 in pure_literals:
                        if pure_literals[var1] != val:
                            del pure_literals[var1]
                    else:
                        pure_literals[var1] = val
                    if var2 in pure_literals:
                        if pure_literals[var2] != val:
                            del pure_literals[var2]
                    else:
                        pure_literals[var2] = val
            else:
                var, val = literal
                if var in pure_literals:
                    if pure_literals[var] != val:
                        del pure_literals[var]
                else:
                    pure_literals[var] = val
    # Assign pure literals
    for var, val in pure_literals.items():
        if var not in assignment:
            assignment[var] = val
            if dpll_satisfiable(clauses, assignment, max_nodes):
                return True
            assignment.pop(var)
            max_nodes += 1
    # Find unit clauses
    unit_clauses = []
    for clause in clauses:
        if len(clause) == 1:
            unit_clauses.append(clause[0])
    # Assign unit clauses
    for literal in unit_clauses:
        if isinstance(literal, tuple):
            if len(literal) == 2:
                var, val = literal
                if var not in assignment:
                    assignment[var] = val
                    if dpll_satisfiable(clauses, assignment, max_nodes):
                        return True
                    assignment.pop(var)
                    max_nodes += 1
            else:
                var1, var2, val = literal
                if var1 not in assignment and var2 not in assignment:
                    assignment[var1] = val
                    assignment[var2] = val
                    if dpll_satisfiable(clauses, assignment, max_nodes):
                        return True
                    assignment.pop(var1)
                    assignment.pop(var2)
                    max_nodes += 1
        else:
            var, val = literal
            if var not in assignment:
                assignment[var] = val
                if dpll_satisfiable(clauses, assignment, max_nodes):
                    return True
                assignment.pop(var)
                max_nodes += 1
    # Choose a variable to split on
    for clause in clauses:
        for literal in clause:
            if isinstance(literal, tuple):
                if len(literal) == 2:
                    var, val = literal
                    if var not in assignment:
                        assignment[var] = val
                        if dpll_satisfiable(clauses, assignment, max_nodes):
                            return True
                        assignment[var] = -val
                        if dpll_satisfiable(clauses, assignment, max_nodes):
                            return True
                        assignment.pop(var)
                        max_nodes += 2
                else:
                    var1, var2, val = literal
                    if var1 not in assignment and var2 not in assignment:
                        assignment[var1] = val
                        assignment[var2] = val
                        if dpll_satisfiable(clauses, assignment, max_nodes):
                            return True
                        assignment[var1] = -val
                        assignment[var2] = -val
                        if dpll_satisfiable(clauses, assignment, max_nodes):
                            return True
                        assignment.pop(var1)
                        assignment.pop(var2)
                        max_nodes += 2
            else:
                var, val = literal
                if var not in assignment:
                    assignment[var] = val
                    if dpll_satisfiable(clauses, assignment, max_nodes):
                        return True
                    assignment[var] = -val
                    if dpll_satisfiable(clauses, assignment, max_nodes):
                        return True
                    assignment.pop(var)
                    max_nodes += 2
    return False

def run_trial(seed):
    n_values = [12, 16, 20]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Generate 3-regular graph
        try:
            edges = generate_3_regular_graph(n, seed)
        except ValueError:
            continue

        # Generate odd charge
        charge = generate_odd_charge(n, seed)

        # Compute phase gap
        nu, delta_Q = compute_phase_gap(edges, n)

        # Generate Tseitin formula
        clauses = tseitin_formula(edges, charge)

        # Run DPLL
        assignment = {}
        t_star = dpll_satisfiable(clauses, assignment)

        # Check conjecture
        if t_star and math.log2(t_star) < nu / 8 - 5:
            conjecture_holds = False
            counterexample = f"n={n}, seed={seed}, t_star={t_star}, nu={nu}"
            break

        metric_values.append(nu)
        instances_tested += 1

    if conjecture_holds:
        metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    else:
        metric_value = 0

    return {
        "metric_name": "nu",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    metric_values = [result["metric_value"] for result in results if result["conjecture_holds"]]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={result['seed']}")
                break
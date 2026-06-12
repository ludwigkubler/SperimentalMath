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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_mult(A, B, mod):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] = (C[i][j] + A[i][l] * B[l][j]) % mod
    return C

def matrix_inv(A, mod):
    n = len(A)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        I[i], I[max_row] = I[max_row], I[i]
        factor = A[i][i]
        for j in range(n):
            A[i][j] = (A[i][j] * pow(factor, mod - 2, mod)) % mod
            I[i][j] = (I[i][j] * pow(factor, mod - 2, mod)) % mod
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % mod
                    I[j][k] = (I[j][k] - factor * I[i][k]) % mod
    return I

def minimal_local_index_of_sheaves(literals, clauses, mod):
    n = len(literals)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    b = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i][i - 1] = 1
        A[i][i] = -1
        b[i] = literals[i]
    for clause in clauses:
        A[0][clause] += 1
        A[0][-1] -= 1
    x = gaussian_elimination(A, b)
    return sum(x[i] * literals[i] for i in range(1, n + 1)) % mod

def generate_d_regular_graph(n, d):
    if (n - 1) * d % 2 != 0:
        raise ValueError("d-regular graph cannot be generated")
    edges = set()
    while len(edges) < (n - 1) * d // 2:
        u, v = random.sample(range(1, n + 1), 2)
        if u > v:
            u, v = v, u
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    return edges

def tseitin_formula(edges):
    literals = {f"x{i}": i for i in range(1, 2 * len(edges))}
    clauses = []
    for u, v in edges:
        a, b = f"x{u}", f"x{v}"
        c = f"y{len(clauses) + 1}"
        literals[c] = len(literals) + 1
        clauses.append([a, -b, c])
        clauses.append([-a, b, c])
        clauses.append([c])
    return literals, clauses

def frege_proof_length(clauses):
    n = max(max(abs(lit) for lit in clause) for clause in clauses)
    proof = []
    for clause in clauses:
        if len(clause) == 1:
            proof.append((clause[0],))
        else:
            a, b, c = clause
            proof.append((a, -b, c))
            proof.append((-a, b, c))
            proof.append((c,))
    return len(proof)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    lrs_values = []
    f_values = []
    for n in n_values:
        try:
            edges = generate_d_regular_graph(n, n - 1)
            literals, clauses = tseitin_formula(edges)
            lrs_value = minimal_local_index_of_sheaves(literals, clauses, mod=2**30 - 1)
            f_value = frege_proof_length(clauses)
            lrs_values.append(lrs_value)
            f_values.append(f_value)
        except Exception as e:
            return {
                "metric_name": "Pearson correlation",
                "metric_value": None,
                "instances_tested": len(lrs_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    if not lrs_values or not f_values:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(lrs_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "lrs(G) or f(φ_G) computation failed"
        }
    mean_lrs = sum(lrs_values) / len(lrs_values)
    mean_f = sum(f_values) / len(f_values)
    correlation = sum((x - mean_lrs) * (y - mean_f) for x, y in zip(lrs_values, f_values)) / (len(lrs_values) * math.sqrt(sum((x - mean_lrs)**2 for x in lrs_values) * sum((y - mean_f)**2 for y in f_values)))
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": len(lrs_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8 and correlation <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    if all(r is not None for r in results):
        mean_metric = sum(results) / len(results)
        support_fraction = sum(1 for r in results if abs(r) >= 0.8 and r <= 3) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std=NA support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation not supported\" first_failing_seed={seeds[results.index(next(r for r in results if abs(r) < 0.8 or r > 3))]}")
    else:
        print("RESULT: INCONCLUSIVE some trials failed")
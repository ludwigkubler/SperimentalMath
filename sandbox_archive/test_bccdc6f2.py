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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += ((-1) ** i) * A[0][i] * determinant(submatrix)
        return det

    def eigenvalues(A):
        n = len(A)
        if n == 2:
            a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
            trace = a + d
            determinant = ad - bc
            lambda1 = (trace + math.sqrt(trace**2 - 4*determinant)) / 2
            lambda2 = (trace - math.sqrt(trace**2 - 4*determinant)) / 2
            return [lambda1, lambda2]
        else:
            # Use QR algorithm for larger matrices
            def qr(A):
                n = len(A)
                Q = [[0 for _ in range(n)] for _ in range(n)]
                R = A[:]
                for i in range(n):
                    Q[i][i] = 1
                for k in range(20):
                    Qk, Rk = gaussian_elimination(matrix_multiply(R, Q)), matrix_multiply(Q, R)
                    Q, R = Qk, Rk
                return Q, R

            Q, R = qr(A)
            eigenvals = [R[i][i] for i in range(n)]
            return eigenvals

    def tseitin_formula(G):
        n = len(G)
        literals = list(range(1, 2*n+1))
        clauses = []
        for i in range(n):
            clauses.append([literals[2*i], literals[2*i+1]])
            for j in range(i+1, n):
                if G[i][j] == 1:
                    clauses.append([-literals[2*i], -literals[2*j+1]])
                    clauses.append([-literals[2*i+1], -literals[2*j]])
        return literals, clauses

    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            p = queue.pop()
            for clause in learned_clauses:
                if any(abs(l) == abs(p[0]) for l in clause):
                    continue
                new_clause = [l for l in clause if l != -p[0]]
                if len(new_clause) == 1:
                    return len(learned_clauses) + 1
                learned_clauses.append(new_clause)
            queue.extend([c for c in clauses if p[0] in c])
        return len(learned_clauses)

    def minimal_order(eigenvals):
        eigenvals.sort()
        min_order = float('inf')
        for i in range(len(eigenvals)):
            order = 1
            for j in range(i+1, len(eigenvals)):
                if abs(eigenvals[j] - eigenvals[i]) < 1e-6:
                    order += 1
                else:
                    break
            min_order = min(min_order, order)
        return min_order

    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            raise ValueError("d * n must be even")
        G = [[0 for _ in range(n)] for _ in range(n)]
        degree_count = [0] * n
        edges_added = 0
        while edges_added < n * d // 2:
            u, v = random.sample(range(n), 2)
            if G[u][v] == 0 and u != v and degree_count[u] < d and degree_count[v] < d:
                G[u][v], G[v][u] = 1, 1
                degree_count[u] += 1
                degree_count[v] += 1
                edges_added += 1
        return G

    def pearson_correlation(X, Y):
        n = len(X)
        mean_X = sum(X) / n
        mean_Y = sum(Y) / n
        cov = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(n)) / n
        std_X = math.sqrt(sum((X[i] - mean_X)**2 for i in range(n)) / n)
        std_Y = math.sqrt(sum((Y[i] - mean_Y)**2 for i in range(n)) / n)
        return cov / (std_X * std_Y)

    def m_order(φ_G):
        eigenvals = eigenvalues(φ_G)
        return minimal_order(eigenvals)

    def w(φ_G):
        literals, clauses = tseitin_formula(φ_G)
        return resolution_width(clauses)

    n_max = 40
    instances_tested = 0
    m_orders = []
    widths = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            G = generate_d_regular_graph(n, 3)
            φ_G = G
            instances_tested += 1
            m_orders.append(m_order(φ_G))
            widths.append(w(φ_G))

    if len(m_orders) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    r = pearson_correlation(m_orders, widths)
    r_squared = r**2

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": r >= 0.8 and r_squared >= 0.9,
        "counterexample": "" if r >= 0.5 else f"r={r:.2f}, |r^2 - 1|={abs(r_squared - 1):.2f}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_r = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_r = math.sqrt(sum((r['metric_value'] - mean_r)**2 for r in results if r['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r:.2f} std={std_r:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r['conjecture_holds'] and r['metric_value'] < 0.5 or abs(r['metric_value']**2 - 1) > 0.1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")
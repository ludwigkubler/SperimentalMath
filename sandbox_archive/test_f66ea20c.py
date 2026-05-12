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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][-1]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def submodular_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        max_val = -float('inf')
        max_col = -1
        for j in range(n):
            if A[i][j] > max_val:
                max_val = A[i][j]
                max_col = j
        if max_val == 0:
            break
        rank += 1
        for j in range(n):
            A[j][max_col] -= A[j][i] * A[max_col][i] / A[i][i]
    return rank

def dpll_solver(clauses, assignment):
    n = len(assignment)
    if not clauses:
        return True
    unit_clause = None
    for clause in clauses:
        if len(clause) == 1:
            unit_clause = clause[0]
            break
    if unit_clause is not None:
        new_assignment = assignment[:]
        new_assignment[abs(unit_clause)-1] = 1 if unit_clause > 0 else -1
        return dpll_solver([c for c in clauses if unit_clause not in c and -unit_clause not in c], new_assignment)
    pure_literal = None
    for i in range(n):
        pos_count, neg_count = 0, 0
        for clause in clauses:
            if i+1 in clause:
                pos_count += 1
            elif -i-1 in clause:
                neg_count += 1
        if pos_count == 0 and neg_count > 0:
            pure_literal = -i-1
        elif neg_count == 0 and pos_count > 0:
            pure_literal = i+1
    if pure_literal is not None:
        new_assignment = assignment[:]
        new_assignment[abs(pure_literal)-1] = 1 if pure_literal > 0 else -1
        return dpll_solver([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment)
    clause = random.choice(clauses)
    literal = random.choice(clause)
    new_assignment = assignment[:]
    new_assignment[abs(literal)-1] = 1 if literal > 0 else -1
    return dpll_solver([c for c in clauses if literal not in c and -literal not in c], new_assignment) or \
           dpll_solver([c for c in clauses if -literal not in c and literal not in c], new_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 3
    submodular_rank_threshold = 0.1 * n
    dnf_size_upper_bound = n**2
    monotone_dnf_rank_upper_bound = 5 * math.log(n)

    def generate_k_clique_instance(n, k):
        edges = []
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                if random.random() < (k / (n-1)):
                    edges.append((i, j))
        return edges

    def incidence_matrix(edges, n):
        A = [[0] * n for _ in range(n)]
        for u, v in edges:
            A[u-1][v-1] = 1
            A[v-1][u-1] = 1
        return A

    def dnf_size(instance):
        clauses = []
        for i in range(1, n+1):
            clause = [i]
            for j in range(i+1, n+1):
                if (i, j) in instance:
                    clause.append(-j)
                else:
                    clause.append(j)
            clauses.append(clause)
        assignment = [0] * n
        return len([c for c in clauses if not any(lit == 0 for lit in c)])

    def is_monotone(instance):
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                if (i, j) in instance and (j, i) not in instance:
                    return False
        return True

    instance = generate_k_clique_instance(n, k)
    A = incidence_matrix(instance, n)
    rank = submodular_rank(A)

    if rank < submodular_rank_threshold or dnf_size(instance) > dnf_size_upper_bound:
        return {
            "metric_name": "submodular_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k-CLIQUE instance with low submodular rank or large DNF size"
        }

    if is_monotone(instance):
        dnf_size_instance = dnf_size(instance)
        if dnf_size_instance > monotone_dnf_rank_upper_bound:
            return {
                "metric_name": "submodular_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "Monotone DNF with large size"
            }

    return {
        "metric_name": "submodular_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 10**9) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"k-CLIQUE instance with low submodular rank or large DNF size\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
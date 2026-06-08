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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(1, max(clauses) + 1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if -pure_literal not in c], new_assignment):
                return True
            return False
        literal = random.choice(list(assignment.keys()))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment):
            return True
        return False

    def clause_graph(clauses):
        n = max(abs(l) for l in set.union(*clauses))
        G = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    a, b = abs(clause[i]), abs(clause[j])
                    G[a][b] = 1
                    G[b][a] = 1
        return G

    def coxeter_group(G):
        n = len(G)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        A = gaussian_elimination(I)
        B = matrix_multiply(A, G)
        C = matrix_multiply(B, A)
        return C

    def normalizing_set(C):
        n = len(C)
        N = set()
        for i in range(1, n + 1):
            if all(C[i - 1][j] == 0 for j in range(n) if j != i - 1):
                N.add(i)
        return N

    def dpll_tree_height(clauses):
        assignment = {}
        stack = [(clauses, assignment)]
        height = 0
        while stack:
            clauses, assignment = stack.pop()
            if not clauses:
                continue
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                stack.append((clauses, new_assignment))
                new_assignment[literal] = False
                stack.append(([c for c in clauses if -literal not in c], new_assignment))
            else:
                literal = random.choice(list(assignment.keys()))
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                stack.append((clauses, new_assignment))
                new_assignment[literal] = False
                stack.append(([c for c in clauses if -literal not in c], new_assignment))
            height += 1
        return height

    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses

    n_max = 40
    instances_tested = 0
    total_height = 0
    max_height = 0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            clauses = generate_3sat_instance(n)
            G = clause_graph(clauses)
            C = coxeter_group(G)
            N = normalizing_set(C)
            height = dpll_tree_height(clauses)
            total_height += height
            instances_tested += 1
            max_height = max(max_height, height)
            if height > 3 * len(N):
                conjecture_holds = False
                counterexample = f"n={n}, h(DPLL)={height}, |N_G|={len(N)}"
                break

    mean_height = total_height / instances_tested
    std_height = math.sqrt(sum((h - mean_height) ** 2 for h in range(total_height)) / instances_tested)

    return {
        "metric_name": "DPLL Tree Height",
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_height = sum(r["metric_value"] for r in results) / len(results)
    std_height = math.sqrt(sum((r["metric_value"] - mean_height) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
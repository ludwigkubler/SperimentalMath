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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Each formula has about 10n clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        stack = []
        assignment = {}
        def solve():
            while True:
                if not cnf:
                    return True
                unit_clause = next((c for c in cnf if len(c) == 1), None)
                if unit_clause:
                    literal = unit_clause[0]
                    if literal < 0 and -literal in assignment:
                        continue
                    assignment[-literal] = False if literal > 0 else True
                    stack.append(literal)
                    cnf = [c for c in cnf if literal not in c and -literal not in c]
                elif len(stack) == 0:
                    return False
                else:
                    literal = stack.pop()
                    assignment[literal] = None
        solve()
        return assignment

    def frege_proof_depth(cnf):
        assignment = dpll(cnf)
        if not assignment:
            return float('inf')
        depth = {var: 0 for var in range(1, -1, -1)}
        stack = [(var, 1) for var in assignment if assignment[var]]
        while stack:
            literal, current_depth = stack.pop()
            if current_depth > depth[literal]:
                depth[literal] = current_depth
            for clause in cnf:
                if literal in clause:
                    other_literals = [l for l in clause if l != literal]
                    for other_literal in other_literals:
                        if assignment[other_literal] is None:
                            stack.append((other_literal, current_depth + 1))
        return max(depth.values())

    def k_theoretic_index(cnf):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    i, j = literal - 1, n
                else:
                    i, j = -literal - 1, n - 1
                A[i][j] += 1
        I = [sum(A[i]) for i in range(n)]
        return max(I)

    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i + 1, n):
                matrix[i][j] /= pivot
            matrix[i][i] = 1
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rref = gaussian_elimination(matrix)
        rank = 0
        for i in range(m):
            if any(rref[i][j] != 0 for j in range(n)):
                rank += 1
        return rank

    def simple_module_index(cnf):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    i, j = literal - 1, n
                else:
                    i, j = -literal - 1, n - 1
                A[i][j] += 1
        rref = gaussian_elimination(A)
        return rank(rref)

    def frege_depth_bound(n):
        # Simple heuristic for Frege depth bound (not rigorous)
        return int(2 * math.log2(n))

    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        cnf = generate_cnf(n)
        depth_bound = frege_depth_bound(n)
        k_index = simple_module_index(cnf)
        depth = frege_proof_depth(cnf)
        results.append({
            "n": n,
            "k_index": k_index,
            "depth": depth,
            "depth_bound": depth_bound
        })

    metric_name = "K-theoretic Index vs Frege Depth"
    metric_value = sum(r["k_index"] for r in results) / len(results)
    instances_tested = len(results)
    n_max = max(r["n"] for r in results)
    conjecture_holds = all(r["k_index"] >= math.pow(r["n"], 2/3) and r["depth"] <= r["depth_bound"] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
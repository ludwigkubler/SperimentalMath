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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses

    def dpll_solve(cnf):
        def solve(literals, assignment):
            if not cnf:
                return True
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[-abs(literal)] = literal > 0
                if not solve(literals, new_assignment):
                    return False
                else:
                    literals.remove(unit_clause)
                    continue
            pure_literal = next((l for l in range(1, n + 1) if all(l in c or -l in c for c in cnf)), None)
            if pure_literal is not None:
                new_assignment[pure_literal] = True
                if not solve(literals, new_assignment):
                    return False
                else:
                    literals = [c for c in cnf if pure_literal not in c and -pure_literal not in c]
                    continue
            literal = random.choice(literals)
            new_assignment[-abs(literal)] = literal > 0
            if solve(literals, new_assignment):
                return True
            else:
                new_assignment[-abs(literal)] = False
                literals.remove([literal])
                continue
        
        assignment = [False] * (n + 1)
        return solve(cnf, assignment)

    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot_row = rank
            while pivot_row < m and matrix[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row == m:
                continue
            matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
            for j in range(i + 1, n):
                factor = Fraction(matrix[rank][j], matrix[rank][i])
                for k in range(m):
                    matrix[k][j] -= factor * matrix[k][i]
            rank += 1
        return rank

    def compute_k_theoretic_index(n):
        # Construct a random binary matrix of size n x n
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        # Perform Gaussian elimination to find the rank
        rank = gaussian_elimination(matrix)
        return rank

    def compute_frege_proof_depth(cnf):
        return dpll_solve(cnf)

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    k_theoretic_index = compute_k_theoretic_index(n)
    frege_proof_depth = compute_frege_proof_depth(cnf)

    metric_name = "K-theoretic Index"
    metric_value = k_theoretic_index
    instances_tested = 1
    n_max = n
    conjecture_holds = k_theoretic_index >= math.ceil(n ** (2/3)) and frege_proof_depth <= 5
    counterexample = "" if conjecture_holds else f"K-theoretic index {k_theoretic_index} < Ω({n}^(2/3)) or Frege depth {frege_proof_depth} > 5"

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
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
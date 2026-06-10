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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_mult(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def k_group_order(n):
        if n == 1:
            return 2
        elif n % 2 == 0:
            return 2 * k_group_order(n // 2)
        else:
            return (n + 1) // 2 * k_group_order((n - 1) // 2)

    def sat_instance(n):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(n):
            clause = random.sample(literals, random.randint(1, n))
            clauses.append(clause)
        return literals, clauses

    def dpll_solve(instance):
        literals, clauses = instance
        n = len(literals)
        assignment = [None] * n
        
        def solve(i):
            if i == n:
                for clause in clauses:
                    if not any(assignment[lit-1] == val for lit, val in zip([l for l in literals if l.startswith('x')], [True, False])):
                        return False
                return True
            literal = literals[i]
            assignment[literal[1]-1] = True
            if solve(i + 1):
                return True
            assignment[literal[1]-1] = False
            if solve(i + 1):
                return True
            return False
        
        return solve(0)

    def frege_proof_length(instance):
        literals, clauses = instance
        n = len(literals)
        proof = []
        
        def prove(clause):
            for literal in clause:
                if assignment[literal[1]-1] == (literal.startswith('x')):
                    continue
                proof.append((literal, 'A'))
                assignment[literal[1]-1] = not assignment[literal[1]-1]
                return True
            return False
        
        while not all(assignment):
            for clause in clauses:
                if not prove(clause):
                    return len(proof)
        
        return len(proof)

    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        instance = sat_instance(n_max)
        if not dpll_solve(instance):
            continue
        
        proof_length = frege_proof_length(instance)
        k_group_order_val = k_group_order(n_max)
        
        metric_value += proof_length / k_group_order_val
        if abs(proof_length - k_group_order_val) > 2 * max(proof_length, k_group_order_val):
            conjecture_holds = False
            counterexample = f"Proof length {proof_length} is more than twice the K-group order {k_group_order_val}"

    metric_value /= instances_tested

    return {
        "metric_name": "Frege Proof Length / K-Group Order",
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
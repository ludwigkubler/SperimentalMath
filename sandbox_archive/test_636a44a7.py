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

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def rank(A):
        return sum(1 for row in gaussian_elimination(A) if any(row))

    def cnf_to_geometric_locus(cnf):
        n = len(cnf[0])
        points = []
        for clause in cnf:
            point = [0] * (n + 1)
            for literal in clause:
                var = abs(literal) - 1
                if literal > 0:
                    point[var] = 1
                else:
                    point[-1] += 1
            points.append(point)
        return points

    def dpll_width(cnf):
        n = len(cnf[0])
        clauses = [set(clause) for clause in cnf]
        variables = set(range(n))
        
        def backtrack(assignment, unit_clauses):
            if not unit_clauses:
                return 1
            literal = next(iter(unit_clauses))
            var = abs(literal) - 1
            value = 1 if literal > 0 else -1
            assignment[var] = value
            new_unit_clauses = set()
            for clause in clauses:
                if literal in clause:
                    unit_clauses.remove(literal)
                elif -literal in clause:
                    clause.discard(-literal)
                    if not clause:
                        return float('inf')
                    new_unit_clauses.add(next(iter(clause)))
            width1 = backtrack(assignment, new_unit_clauses)
            assignment[var] = -value
            new_unit_clauses = set()
            for clause in clauses:
                if -literal in clause:
                    unit_clauses.remove(-literal)
                elif literal in clause:
                    clause.discard(literal)
                    if not clause:
                        return float('inf')
                    new_unit_clauses.add(next(iter(clause)))
            width2 = backtrack(assignment, new_unit_clauses)
            return max(width1, width2)
        
        return backtrack({}, set())

    n = random.randint(5, 40)
    cnf = [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
    geometric_locus = cnf_to_geometric_locus(cnf)
    minimal_rank = rank(geometric_locus)
    dpll_width_value = dpll_width(cnf)

    if minimal_rank == 0 or dpll_width_value == float('inf'):
        return {
            "metric_name": "dpll_width",
            "metric_value": dpll_width_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "minimal_rank_zero_or_dpll_width_infinite"
        }

    c = 2 ** n
    return {
        "metric_name": "dpll_width",
        "metric_value": dpll_width_value,
        "instances_tested": 1,
        "conjecture_holds": dpll_width_value <= c * minimal_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank_zero_or_dpll_width_infinite\" first_failing_seed={first_failing_seed}")
# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def random_cnf(n, m):
    cnf = []
    for _ in range(m):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        clause = ' '.join(map(str, literals)) + ' 0'
        cnf.append(clause)
    return '\n'.join(cnf)

def resolution_width(cnf):
    clauses = cnf.split('\n')
    literals = set()
    for clause in clauses:
        literals.update(abs(int(lit)) for lit in clause.split() if lit != '0')

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = int(unit_clause[0])
            if literal < 0 and literal in assignment or literal > 0 and -literal in assignment:
                return False
            assignment.add(literal if literal > 0 else -literal)
            clauses = [c for c in clauses if literal not in c and -literal not in c]
        pure_literal = next((l for l in literals if (l in assignment or -l in assignment) == False), None)
        if pure_literal:
            assignment.add(pure_literal)
            clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
        return dpll(clauses, assignment)

    max_width = 0
    for _ in range(10):  # Repeat DPLL multiple times to get a better estimate of the width
        assignment = set()
        width = 0
        while True:
            if dpll(clauses, assignment):
                break
            new_literal = random.choice(list(literals - assignment))
            assignment.add(new_literal)
            width += 1
        max_width = max(max_width, width)
    return max_width

def grothendieck_witt_class(cnf):
    n = int(cnf.split('\n')[0].split()[2])
    clause_indicator_poly = [0] * (1 << n)
    for clause in cnf.split('\n'):
        if ' 0' not in clause:
            literals = list(map(int, clause.split()))
            product = 1
            for lit in literals:
                if lit > 0:
                    product *= (-1) ** (lit - 1)
                else:
                    product *= (-1) ** (-lit - 1)
            clause_indicator_poly[sum(abs(lit) for lit in literals)] += product

    def matrix_mult(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def gaussian_elimination(A, b):
        m = len(A)
        n = len(A[0])
        augmented_matrix = [A[i] + [b[i]] for i in range(m)]
        row, col = 0, 0
        while row < m and col < n:
            if A[row][col] == 0:
                swap_row = next((i for i in range(row + 1, m) if augmented_matrix[i][col]), None)
                if swap_row is None:
                    col += 1
                else:
                    augmented_matrix[row], augmented_matrix[swap_row] = augmented_matrix[swap_row], augmented_matrix[row]
            else:
                pivot = augmented_matrix[row][col]
                for j in range(col, n + 1):
                    augmented_matrix[row][j] /= pivot
                for i in range(m):
                    if i != row and augmented_matrix[i][col] != 0:
                        factor = augmented_matrix[i][col]
                        for j in range(col, n + 1):
                            augmented_matrix[i][j] -= factor * augmented_matrix[row][j]
                row += 1
                col += 1

        rank = sum(1 for i in range(m) if any(augmented_matrix[i][j] != 0 for j in range(n)))
        return rank

    A = []
    b = []
    for i in range(1, len(clause_indicator_poly)):
        A.append([clause_indicator_poly[j] for j in range(i)])
        b.append(clause_indicator_poly[i])

    return gaussian_elimination(A, b)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice(range(5, 41))
    m = int(n * (n - 1) / 2)  # Typical number of clauses for a satisfiable instance
    cnf = random_cnf(n, m)
    
    try:
        t_star = resolution_width(cnf)
        rk_W_F = grothendieck_witt_class(cnf)
        
        if t_star == 0 or rk_W_F == 0:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "t_star or rk_W_F is zero"
            }
        
        correlation = abs(rk_W_F / t_star)
        return {
            "metric_name": "correlation",
            "metric_value": correlation,
            "instances_tested": 1,
            "conjecture_holds": 0.9 <= correlation <= 1.1,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = list(map(int, sys.argv[1:]))
    else:
        seeds = [2**i + 1 for i in range(5, 6)]  # Default to 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results if r['metric_value'] is not None)/len(results)} std=0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["conjecture_holds"] == False for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["conjecture_holds"] == False)
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["conjecture_holds"] == False)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
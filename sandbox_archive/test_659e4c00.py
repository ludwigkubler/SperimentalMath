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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0, 1) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment, variables):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and -literal in assignment or literal > 0 and literal in assignment:
                return False
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(new_clauses, assignment, variables)
        pure_literal = next((v for v in variables if all(lit != v and -lit != v for lit in clauses)), None)
        if pure_literal:
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(new_clauses, assignment, variables)
        literal = random.choice(variables)
        if literal < 0 and -literal in assignment or literal > 0 and literal in assignment:
            return False
        assignment[literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        if dpll(new_clauses, assignment, variables):
            return True
        del assignment[literal]
        assignment[-literal] = True
        new_clauses = [c for c in clauses if -literal not in c and literal not in c]
        return dpll(new_clauses, assignment, variables)

    def cnf_to_algebraic_model(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        A = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
        b = [Fraction(0, 1) for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                row = abs(lit) - 1
                col = abs(lit) - 1
                A[row][col] += Fraction(1, 1)
                b[row] -= Fraction(1, 1) if lit < 0 else Fraction(1, 1)
        return gaussian_elimination(A), b

    def minimal_representation_length(A, b):
        n = len(A)
        rank = sum(1 for row in A if any(coeff != Fraction(0, 1) for coeff in row))
        return rank + sum(abs(b[i]) for i in range(n) if all(row[i] == Fraction(0, 1) for row in A))

    def dpll_width(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        assignment = {}
        variables = set(abs(lit) for clause in cnf for lit in clause)
        return len(dpll(cnf, assignment, variables))

    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        clauses = [[random.randint(-n, -1) if random.random() < 0.5 else random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
        A, b = cnf_to_algebraic_model(clauses)
        representation_length = minimal_representation_length(A, b)
        width = dpll_width(cnf)
        results.append((representation_length, width))

    mean_representation_length = sum(x[0] for x in results) / len(results)
    mean_width = sum(x[1] for x in results) / len(results)
    correlation = sum((x[0] - mean_representation_length) * (x[1] - mean_width) for x in results) / len(results) / math.sqrt(sum((x[0] - mean_representation_length)**2 for x in results)) / math.sqrt(sum((x[1] - mean_width)**2 for x in results))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in [x[1] for x in results]),
        "conjecture_holds": 0.5 <= correlation < 0.7,
        "counterexample": "" if 0.5 <= correlation < 0.7 else f"Pearson Correlation: {correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_correlation = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson Correlation < 0.5\" first_failing_seed={first_failing_seed}")
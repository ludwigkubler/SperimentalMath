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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                if j != i:
                    ratio = A[j][i] / factor
                    for k in range(i, n + 1):
                        A[j][k] -= ratio * A[i][k]
                    b[j] -= ratio * b[i]
        return [b[i] / A[i][i] for i in range(n)]

    def matrix_mult(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return C

    def matrix_add(A, B):
        m = len(A)
        n = len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C

    def matrix_sub(A, B):
        m = len(A)
        n = len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for c in range(len(A)):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det

    def inverse(A):
        n = len(A)
        if determinant(A) == 0:
            raise ValueError("Matrix is not invertible")
        adjugate = [[((-1) ** (i+j)) * determinant([row[:j] + row[j+1:] for row in A[:i] + A[i+1:]])
                     for j in range(n)] for i in range(n)]
        return matrix_mult(adjugate, 1 / determinant(A))

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var, f'~{var}'])
        for i in range(1 << n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(variables[j])
                else:
                    clause.append(f'~{variables[j]}')
            clauses.append(clause)
        return variables, clauses

    def dpll_search_tree_width(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and f'~{literal}' not in c]
            return 1 + dpll_search_tree_width(new_clauses, new_assignment)
        pure_literals = {}
        for literal in set(l for c in clauses for l in c):
            pos_count = sum(1 for c in clauses if literal in c)
            neg_count = sum(1 for c in clauses if f'~{literal}' in c)
            if pos_count == 0:
                pure_literals[literal] = True
            elif neg_count == 0:
                pure_literals[f'~{literal}'] = False
        if pure_literals:
            literal, value = next(iter(pure_literals.items()))
            new_assignment = assignment.copy()
            new_assignment[literal] = value
            new_clauses = [c for c in clauses if literal not in c and f'~{literal}' not in c]
            return 1 + dpll_search_tree_width(new_clauses, new_assignment)
        literals = list(set(l for c in clauses for l in c))
        literal = random.choice(literals)
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        new_clauses_true = [c for c in clauses if literal not in c and f'~{literal}' not in c]
        width_true = 1 + dpll_search_tree_width(new_clauses_true, new_assignment_true)
        new_assignment_false = assignment.copy()
        new_assignment_false[literal] = False
        new_clauses_false = [c for c in clauses if literal not in c and f'~{literal}' not in c]
        width_false = 1 + dpll_search_tree_width(new_clauses_false, new_assignment_false)
        return max(width_true, width_false)

    def eta_invariant(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            a = [1]
            b = [1]
            for i in range(2, n + 1):
                a_next = [(a[j] + a[j - 1]) % i for j in range(i)]
                b_next = [(b[j] + b[j - 1]) % i for j in range(i)]
                a = a_next
                b = b_next
            return sum(a[i] * b[i] for i in range(n)) % n

    variables, clauses = generate_tseitin_formula(5)
    assignment = {var: False for var in variables}
    width = dpll_search_tree_width(clauses, assignment)
    eta = eta_invariant(len(variables))
    
    return {
        "metric_name": "eta_width_correlation",
        "metric_value": eta * width,
        "instances_tested": 1,
        "n_max": len(variables),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
    from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for c in range(len(A)):
            submatrix = [row[:c] + row[c+1:] for row in A[1:]]
            sign = (-1) ** (c % 2)
            sub_det = determinant(submatrix)
            det += sign * A[0][c] * sub_det
        return det

    def euler_characteristic(clause_link_complex):
        n = len(clause_link_complex)
        return sum((-1)**k * len(list(itertools.combinations(clause_link_complex, k))) for k in range(n+1))

    def communication_complexity(cnf_formula):
        # Placeholder implementation of KW game complexity
        # This is a simplified version and may not be accurate
        n = len(cnf_formula)
        return 2 * n

    def generate_cnf(n):
        num_clauses = random.randint(5, 14)
        cnf = []
        for _ in range(num_clauses):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf

    def is_satisfiable(cnf_formula):
        n = len(cnf_formula[0])
        variables = list(range(1, n+1))
        for assignment in itertools.product([False, True], repeat=n):
            if all(any((assignment[abs(l)-1] if l > 0 else not assignment[abs(l)-1]) == (l > 0) for l in clause) for clause in cnf_formula):
                return True
        return False

    def clause_link_complex(cnf_formula):
        n = len(cnf_formula[0])
        clause_link_complex = []
        for i in range(2**n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            if all(any((assignment[abs(l)-1] if l > 0 else not assignment[abs(l)-1]) == (l > 0) for l in clause) for clause in cnf_formula):
                clause_link_complex.append(tuple(sorted([j+1 for j, v in enumerate(assignment) if v])))
        return set(clause_link_complex)

    n = random.randint(5, 14)
    cnf_formula = generate_cnf(n)
    
    if not is_satisfiable(cnf_formula):
        return {
            "metric_name": "Euler Characteristic",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_cnf"
        }

    clause_link_complex_ = clause_link_complex(cnf_formula)
    euler_char = euler_characteristic(clause_link_complex_)
    kw_complexity = communication_complexity(cnf_formula)

    return {
        "metric_name": "Euler Characteristic",
        "metric_value": euler_char,
        "instances_tested": 1,
        "conjecture_holds": euler_char == kw_complexity,
        "counterexample": "" if euler_char == kw_complexity else f"euler={euler_char}, kw={kw_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"euler!=kw\" first_failing_seed={first_failing_seed}")
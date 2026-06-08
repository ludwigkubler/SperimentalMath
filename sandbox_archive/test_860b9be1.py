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

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det

    def symplectic_form(M):
        n = len(M)
        I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        J = [[Fraction(0), Fraction(1)] + [Fraction(0)]*(n-2),
             [-Fraction(1), Fraction(0)] + [Fraction(0)]*(n-2)]
        J += [[Fraction(0)]*i + [Fraction(0)] + [Fraction(-1) if j == i+1 else Fraction(0) for j in range(i, n-1)] + [Fraction(0)] for i in range(n-2)]
        return determinant(gaussian_elimination(M + J))

    def dpll(instance):
        def backtrack(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal < 0 and -literal in assignment:
                    return False
                assignment[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                if backtrack(new_clauses, assignment):
                    return True
                del assignment[literal]
            else:
                literal = next((i for i in range(1, len(instance) + 1) if i not in assignment), None)
                assignment[literal] = True
                if backtrack(clauses, assignment):
                    return True
                del assignment[literal]
                assignment[-literal] = True
                if backtrack(clauses, assignment):
                    return True
                del assignment[-literal]
            return False

        clauses = instance
        assignment = {}
        return backtrack(clauses, assignment)

    def generate_instance(n):
        return [[random.choice([1, -1]) for _ in range(2*n)] for _ in range(2*n)]

    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        instance = generate_instance(n)
        M = [[sum(row[i] * row[j] for i in range(2*n)) for j in range(2*n)] for row in instance]
        msl = dpll(instance)
        symplectic_val = symplectic_form(M)

        results.append({
            "n": n,
            "msl": msl,
            "symplectic_val": symplectic_val
        })

    if not results:
        return {
            "metric_name": "log_symplectic_form",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }

    log_msl = [math.log(result["msl"]) for result in results if result["msl"] > 0]
    log_symplectic_val = [math.log(result["symplectic_val"]) for result in results if result["symplectic_val"] > 0]

    if not log_msl or not log_symplectic_val:
        return {
            "metric_name": "log_symplectic_form",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "zero_values"
        }

    mean_msl = sum(log_msl) / len(log_msl)
    mean_symplectic_val = sum(log_symplectic_val) / len(log_symplectic_val)

    return {
        "metric_name": "log_symplectic_form",
        "metric_value": mean_symplectic_val,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(mean_msl - 2 * math.log(n)) < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_msl = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_msl)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] is not None and abs(result["metric_value"] - 2 * math.log(n)) < 0.5 for n, result in zip([result["n"] for result in results], results)):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds'] and abs(result['metric_value'] - 2 * math.log(n)) < 0.5))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
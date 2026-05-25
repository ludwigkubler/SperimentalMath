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
    
    def generate_tseitin_clause_set(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clause = [i]
            for j in range(i + 1, n + 1):
                clause.append(-j)
            clauses.append(clause)
            clauses.append([-i] + list(range(j + 1, n + 1)))
        return variables, clauses

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
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
            return None
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def minimal_index_of_kahler_metric(clause_set):
        variables = set()
        for clause in clause_set:
            variables.update(abs(x) for x in clause if x != 0)
        n = len(variables)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, var in enumerate(variables):
            A[i][i] = 1
            for clause in clause_set:
                if var in clause:
                    for x in clause:
                        if abs(x) != var and x != 0:
                            A[i][variables.index(abs(x))] += 1
        A = gaussian_elimination(A)
        det = determinant(A)
        return abs(det)

    def resolution_refutation(clause_set):
        clauses = list(clause_set)
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i = set(clauses[i])
                    clause_j = set(clauses[j])
                    if -clauses[i][0] in clauses[j]:
                        new_clause = list(clause_i ^ clause_j)
                        if not any(x in new_clause for x in variables):
                            return len(new_clause) + 1
                        new_clauses.append(new_clause)
            if new_clauses == clauses:
                return None
            clauses += new_clauses

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        variables, clause_set = generate_tseitin_clause_set(n)
        kahler_index = minimal_index_of_kahler_metric(clause_set)
        refutation_length = resolution_refutation(clause_set)
        if refutation_length is None:
            continue
        results.append({
            "n": n,
            "kahler_index": kahler_index,
            "refutation_length": refutation_length
        })

    if not results:
        return {
            "metric_name": "minimal_kahler_index",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_kahler_index = sum(result["kahler_index"] for result in results) / len(results)
    max_refutation_length = max(result["refutation_length"] for result in results)

    return {
        "metric_name": "minimal_kahler_index",
        "metric_value": mean_kahler_index,
        "instances_tested": len(results),
        "conjecture_holds": all(result["kahler_index"] <= 2 ** result["refutation_length"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
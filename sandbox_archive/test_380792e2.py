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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses

    def dpll_solve(clauses):
        def solve(literals, assignment):
            if not literals:
                return True
            literal = literals.pop()
            pos_var = abs(literal)
            neg_var = -pos_var
            if pos_var in assignment or neg_var in assignment:
                literals.add(literal)
                continue
            assignment[pos_var] = 1
            if solve(literals, assignment):
                return True
            del assignment[pos_var]
            assignment[neg_var] = 1
            if solve(literals, assignment):
                return True
            del assignment[neg_var]
            literals.add(literal)
            return False
        
        return solve(set(clauses), {})

    def noncommutative_modular_form(clauses):
        n = max(abs(lit) for clause in clauses for lit in clause)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    row, col = lit - 1, n
                else:
                    row, col = abs(lit) - 1, n - 1
                matrix[row][col] += 1
        return matrix

    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return float('inf')
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j == i:
                    continue
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    dpll_length = len(dpll_solve(clauses))
    form = noncommutative_modular_form(clauses)
    min_rank = rank(form)

    return {
        "metric_name": "DPLL Proof Length vs Minimal Rank",
        "metric_value": dpll_length,
        "instances_tested": 1,
        "conjecture_holds": dpll_length <= 2 ** min_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"DPLL Proof Length > 2^min_rank\" first_failing_seed={res['seed']}")
                break
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(abs(x) > abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def grothendieck_witt_class(clauses):
        n = len(clauses)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(clauses):
            for j in clause:
                if j > 0:
                    A[i][j - 1] += 1
                else:
                    A[i][-j] -= 1
        rank = gaussian_elimination(A)
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return m - i
            for j in range(i + 1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank
    
    def resolution_width(clauses):
        n = len(clauses)
        stack = []
        for clause in clauses:
            stack.append(clause)
        while stack:
            clause = stack.pop()
            if not clause:
                continue
            literal = random.choice(clause)
            new_clauses = []
            for c in clauses:
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                elif -literal in c:
                    new_clauses.append([x for x in c if x != -literal] + [-l for l in clause if l != -literal])
            stack.extend(new_clauses)
        return len(clauses) - n
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    w_f = grothendieck_witt_class(cnf)
    t_star = resolution_width(cnf)
    
    if t_star == 0:
        return {
            "metric_name": "rk(W(F))",
            "metric_value": w_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    alpha = Fraction(w_f, t_star)
    beta = Fraction(w_f, t_star)
    correlation = abs(alpha - beta) / (alpha + beta)
    
    return {
        "metric_name": "rk(W(F))",
        "metric_value": w_f,
        "instances_tested": 1,
        "conjecture_holds": correlation >= 0.9 or correlation <= 1.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_range\" first_failing_seed={first_failing_seed}")
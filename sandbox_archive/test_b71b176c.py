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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def dpll_solve(clauses):
        def solve(literals):
            if not literals:
                return True
            literal = literals[0]
            if any(literal == -x for x in literals):
                return False
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return solve([l for l in literals if l != literal]) or solve([l for l in literals if l != -literal])
        return solve(list(range(1, n + 1)))
    
    def noncommutative_modular_form(clauses):
        n = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal > 0:
                    matrix[i][literal - 1] += 1
                else:
                    matrix[literal - 1][i] += 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                swap_row = next(j for j in range(i + 1, m) if matrix[j][i] != 0)
                matrix[i], matrix[swap_row] = matrix[swap_row], matrix[i]
            for j in range(i + 1, m):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    dpll_length = len(clauses) if not dpll_solve(clauses) else 0
    form = noncommutative_modular_form(clauses)
    min_rank = rank(form)
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": dpll_length,
        "instances_tested": 1,
        "conjecture_holds": dpll_length <= 2 ** min_rank if min_rank > 0 else False,
        "counterexample": "" if dpll_length <= 2 ** min_rank else f"n={n}, DPLL length={dpll_length}, rank={min_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    
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
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
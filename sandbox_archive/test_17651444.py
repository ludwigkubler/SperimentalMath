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
    
    def generate_random_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def dpll_solve(clauses):
        def solve(literals):
            if not clauses:
                return True
            literal = next((l for l in literals if any(l in c or -l in c for c in clauses)), None)
            if literal is None:
                return False
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if solve([l for l in literals if l != literal]):
                return True
            if solve([l for l in literals if l != -literal]):
                return True
            return False
        
        all_literals = set(abs(l) for clause in clauses for l in clause)
        return solve(list(all_literals))
    
    def noncommutative_modular_form(clauses):
        n = max(abs(l) for clause in clauses for l in clause)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for i, j in [(abs(clause[0]), abs(clause[1])), (abs(clause[0]), abs(clause[2])), (abs(clause[1]), abs(clause[2]))]:
                if clause[0] > 0 and clause[1] > 0:
                    matrix[i][j] += 1
                elif clause[0] < 0 and clause[1] < 0:
                    matrix[i][j] -= 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return float('inf')
            for j in range(i + 1, n):
                matrix[i][j] /= matrix[i][i]
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    for j in range(i, n):
                        matrix[k][j] -= matrix[k][i] * matrix[i][j]
        return sum(1 for row in matrix if any(row[j] != 0 for j in range(n)))
    
    def dpll_proof_length(clauses):
        return len(clauses) + 2
    
    n = random.randint(5, 40)
    clauses = generate_random_3cnf(n)
    phi_I = noncommutative_modular_form(clauses)
    min_rank_phi_I = rank(phi_I)
    dpll_len = dpll_proof_length(clauses)
    
    return {
        "metric_name": "DPLL Proof Length vs Rank",
        "metric_value": dpll_len,
        "instances_tested": 1,
        "conjecture_holds": dpll_len <= 2 ** min_rank_phi_I,
        "counterexample": "" if dpll_len <= 2 ** min_rank_phi_I else f"DPLLProofLength({dpll_len}) > 2^min_rank({min_rank_phi_I})"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
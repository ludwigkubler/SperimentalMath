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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                continue
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses):
        n = len(clauses[0])
        polynomial = [0] * (2**n)
        for clause in clauses:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (1 - x[literal-1])
                else:
                    term *= (x[-literal-1])
            polynomial[sum(abs(lit) for lit in clause)] += term
        return polynomial
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = -1
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(rows):
                if j != rank and matrix[j][i] != 0:
                    factor = matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def dpll_search_tree_width(clauses):
        n = len(clauses[0])
        def backtrack(model, clause_index):
            if clause_index == len(clauses):
                return True
            for literal in clauses[clause_index]:
                if literal > 0 and literal not in model:
                    model.add(literal)
                    if backtrack(model, clause_index + 1):
                        return True
                    model.remove(literal)
                elif literal < 0 and -literal not in model:
                    model.add(-literal)
                    if backtrack(model, clause_index + 1):
                        return True
                    model.remove(-literal)
            return False
        return max(len(backtrack(set(), i)) for i in range(len(clauses)))
    
    n = random.randint(5, 40)
    clauses = generate_sat_instance(n)
    polynomial = clause_indicator_polynomial(clauses)
    matrix = [[polynomial[i] for i in range(2**n)]]
    rank = gaussian_elimination(matrix)
    dpll_width = dpll_search_tree_width(clauses)
    
    f_n = math.sqrt(n) * math.log(n)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= f_n,
        "counterexample": "" if rank <= f_n else f"n={n}, dPLL width={dpll_width}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")
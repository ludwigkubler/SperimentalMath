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
    
    def generate_k_cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k * n):
            clause = set()
            while len(clause) < k:
                var = random.choice(variables)
                if -var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def tseitin_matrix(clauses, variables):
        literals = {f"x{i}": i for i in range(1, len(variables) + 1)}
        neg_literals = {f"-x{i}": -i for i in range(1, len(variables) + 1)}
        matrix = []
        for clause in clauses:
            row = [0] * (2 * len(variables))
            for literal in clause:
                if literal > 0:
                    row[literals[f"x{literal}"] - 1] = 1
                else:
                    row[neg_literals[f"-x{-literal}"] - 1] = 1
            matrix.append(row)
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[i][j] == 0 for j in range(m)):
                continue
            pivot_col = next(j for j in range(m) if matrix[i][j] != 0)
            for j in range(i + 1, n):
                factor = -matrix[j][pivot_col] / matrix[i][pivot_col]
                for k in range(m):
                    matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def dpll_search_tree_height(clauses):
        def dpll(clauses, assignment):
            if not clauses:
                return True
            literal = next(lit for lit in range(1, len(variables) + 1) if lit not in assignment and -lit not in assignment)
            pos_assignment = assignment.copy()
            neg_assignment = assignment.copy()
            pos_assignment[literal] = True
            neg_assignment[-literal] = True
            return dpll(clauses, pos_assignment) or dpll(clauses, neg_assignment)
        return len(variables) if dpll(clauses, {}) else 0
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 10))
    clauses = generate_k_cnf(n, k)
    matrix = tseitin_matrix(clauses, list(range(1, n + 1)))
    minimal_rank = gaussian_elimination(matrix)
    dpll_height = dpll_search_tree_height(clauses)
    
    expected_rank = math.log(n) / math.log(k)
    within_margin = abs(minimal_rank - expected_rank) <= 0.1 * expected_rank
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": within_margin and dpll_height == math.ceil(expected_rank),
        "counterexample": "" if within_margin and dpll_height == math.ceil(expected_rank) else f"Rank: {minimal_rank}, Height: {dpll_height}, Expected: {math.ceil(expected_rank)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
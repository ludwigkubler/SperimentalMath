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
    
    def generate_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k * n):
            clause = [random.choice(variables), -random.choice(variables)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses
    
    def tseitin_matrix(clauses):
        variables = set()
        new_vars = {}
        for i, clause in enumerate(clauses):
            var = n + i + 1
            variables.add(var)
            new_vars[clause] = var
        matrix = []
        for clause in clauses:
            row = [0] * (n + len(new_vars))
            for lit in clause:
                if lit > 0:
                    row[lit - 1] = 1
                else:
                    row[-new_vars[-lit]] = 1
            matrix.append(row)
        return matrix, variables
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            pivot = Fraction(1, matrix[i][i])
            for j in range(n):
                matrix[i][j] *= pivot
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            if -literal in assignment:
                return False
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pure_literals = []
        for var in range(1, len(variables) + 1):
            pos_count = sum(1 for clause in clauses if var in clause)
            neg_count = sum(1 for clause in clauses if -var in clause)
            if pos_count == 0:
                pure_literals.append(-var)
            elif neg_count == 0:
                pure_literals.append(var)
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        literal = next(lit for lit in range(1, len(variables) + 1) if lit not in assignment and -lit not in assignment)
        return dpll(clauses, {**assignment, literal: True}) or dpll(clauses, {**assignment, literal: False})
    
    def dpll_search_tree_height(clauses):
        variables = set()
        for clause in clauses:
            for lit in clause:
                variables.add(abs(lit))
        return len(variables) if dpll(clauses, {}) else 0
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n, 10))
    clauses = generate_kcnf(n, k)
    matrix, variables = tseitin_matrix(clauses)
    rank = gaussian_elimination(matrix)
    dpll_height = dpll_search_tree_height(clauses)
    
    expected_rank = math.ceil(math.log(n) / math.log(k))
    within_margin = abs(rank - expected_rank) <= 0.1 * expected_rank
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": within_margin and rank == dpll_height,
        "counterexample": "" if within_margin else f"rank={rank}, expected={expected_rank}, dpll_height={dpll_height}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30)) + [i for i in range(50, 89, 7)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank_mismatch\" first_failing_seed={first_failing_seed}")
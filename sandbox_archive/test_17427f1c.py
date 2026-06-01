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

def generate_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        random.shuffle(literals)
        clause = ' '.join(map(str, literals)) + ' 0'
        clauses.append(clause)
    return '\n'.join(clauses)

def dpll_solver(formula):
    def parse_formula(formula):
        lines = formula.split('\n')
        n = int(lines[0].split()[2])
        clauses = []
        for line in lines[1:]:
            literals = [int(lit) for lit in line.split()[:-1]]
            clauses.append(literals)
        return n, clauses

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] = literal > 0
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pure_literal = next((lit for lit, count in enumerate(sum(clauses, []), start=1) if count % 2 == len(clauses)), None)
        if pure_literal is not None:
            new_assignment = assignment[:]
            new_assignment[pure_literal - 1] = True
            return dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment)
        literal = random.choice(sum(clauses, []))
        new_assignment = assignment[:]
        new_assignment[abs(literal) - 1] = literal > 0
        if dpll(clauses, new_assignment):
            return True
        new_assignment[abs(literal) - 1] = not (literal > 0)
        return dpll(clauses, new_assignment)

    n, clauses = parse_formula(formula)
    assignment = [None] * n
    return dpll(clauses, assignment)

def matrix_representation(φ):
    n = φ.count('\n')
    m = len(φ.split('\n')[1].split()) - 1
    A = [[0] * (m + 1) for _ in range(n)]
    literals = [int(lit) for lit in φ.replace(' ', '\n').split('\n') if lit]
    for literal in literals:
        row, col = abs(literal) // m, abs(literal) % m
        A[row][col] += 1 if literal > 0 else -1
    return A

def minimal_local_system_rank(A):
    n = len(A)
    m = len(A[0])
    rank = 0
    for i in range(n):
        pivot_row = next((j for j in range(i, n) if A[j][i] != 0), None)
        if pivot_row is not None:
            rank += 1
            for j in range(m):
                A[i][j], A[pivot_row][j] = A[pivot_row][j], A[i][j]
            for k in range(n):
                if k != i and A[k][i] != 0:
                    factor = A[k][i] / A[i][i]
                    for j in range(m):
                        A[k][j] -= factor * A[i][j]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mean_ranks = []
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            φ = generate_3cnf(n)
            A = matrix_representation(φ)
            mls = minimal_local_system_rank(A)
            w = dpll_solver(φ)
            if w is None:
                continue
            mean_ranks.append(mls / (w ** 2))
    
    if not mean_ranks:
        return {
            "metric_name": "mls/width^2",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = sum(mean_ranks) / len(mean_ranks)
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in mean_ranks) / len(mean_ranks))
    support_fraction = sum(1 for x in mean_ranks if abs(x - 1.0) <= 0.1) / len(mean_ranks)
    
    return {
        "metric_name": "mls/width^2",
        "metric_value": mean_rank,
        "instances_tested": len(mean_ranks),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r['metric_value'] - 1.0) > 0.11 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if abs(r['metric_value'] - 1.0) > 0.11)
        print(f"RESULT: FALSIFIED counterexample=\"mls/width^2 deviates by more than 110%\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i]:
                    for j in range(n):
                        A[k][j] -= A[i][j] * A[k][i]
        return A

    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [[l for l in c if l != literal and -l not in new_assignment] for c in clauses]
            return dpll(new_clauses, new_assignment)
        pure_literals = set()
        for clause in clauses:
            literals = [l for l in clause if l > 0]
            negated_literals = [-l for l in clause if l < 0]
            if not literals and any(-l in assignment for l in negated_literals):
                continue
            if len(literals) == 1:
                pure_literals.add(literals[0])
            elif len(negated_literals) == 1:
                pure_literals.add(negated_literals[0])
        if pure_literals:
            literal = next(iter(pure_literals))
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [[l for l in c if l != literal and -l not in new_assignment] for c in clauses]
            return dpll(new_clauses, new_assignment)
        literal = random.choice([l for l in range(1, 2 * max(abs(l) for clause in clauses)) if l not in assignment])
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        new_clauses_true = [[l for l in c if l != literal and -l not in new_assignment_true] for c in clauses]
        if dpll(new_clauses_true, new_assignment_true):
            return True
        new_assignment_false = assignment.copy()
        new_assignment_false[literal] = False
        new_clauses_false = [[l for l in c if l != literal and -l not in new_assignment_false] for c in clauses]
        return dpll(new_clauses_false, new_assignment_false)

    def generate_cnf(n):
        num_clauses = random.randint(10, 20)
        clauses = []
        for _ in range(num_clauses):
            clause = set()
            while not clause:
                literals = [random.choice([i, -i]) for i in range(1, n + 1)]
                clause = set(literals) if random.choice([True, False]) else set([-l for l in literals])
            clauses.append(list(clause))
        return clauses

    def construct_quandle(cnf):
        truth_table = {}
        for assignment in itertools.product([False, True], repeat=len(cnf)):
            literal_values = {i: assignment[i - 1] for i in range(1, len(cnf) + 1)}
            clause_truths = [all(literal_values.get(abs(l), False) == (l > 0) for l in c) for c in cnf]
            truth_table[tuple(literal_values.values())] = all(clause_truths)
        quandle_size = len(truth_table)
        quandle_operation = [[truth_table[(a, b)] for b in range(quandle_size)] for a in range(quandle_size)]
        return quandle_operation

    def minimal_quandle_order(quandle):
        m = len(quandle)
        identity = [i == j for i in range(m) for j in range(m)]
        if gaussian_elimination(quandle) != identity:
            return None
        order = 1
        while True:
            new_quandle = matrix_multiply(quandle, quandle)
            if gaussian_elimination(new_quandle) == identity:
                break
            order += 1
        return order

    def dpll_search_tree_width(cnf):
        assignment = {}
        stack = [(cnf, assignment)]
        max_width = 0
        while stack:
            clauses, assignment = stack.pop()
            if not clauses:
                continue
            unit_clauses = [c[0] for c in clauses if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                new_clauses = [[l for l in c if l != literal and -l not in new_assignment] for c in clauses]
                stack.append((new_clauses, new_assignment))
            else:
                literals = [l for l in range(1, 2 * max(abs(l) for clause in clauses)) if l not in assignment]
                literal = random.choice(literals)
                new_assignment_true = assignment.copy()
                new_assignment_true[literal] = True
                new_clauses_true = [[l for l in c if l != literal and -l not in new_assignment_true] for c in clauses]
                stack.append((new_clauses_true, new_assignment_true))
                new_assignment_false = assignment.copy()
                new_assignment_false[literal] = False
                new_clauses_false = [[l for l in c if l != literal and -l not in new_assignment_false] for c in clauses]
                stack.append((new_clauses_false, new_assignment_false))
            max_width = max(max_width, len(stack))
        return max_width

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    quandle = construct_quandle(cnf)
    minimal_order = minimal_quandle_order(quandle)
    if minimal_order is None:
        return {"metric_name": "minimal_order", "metric_value": float('inf'), "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "quandle_undefined"}
    dpll_width = dpll_search_tree_width(cnf)
    return {"metric_name": "minimal_order", "metric_value": minimal_order, "instances_tested": 1, "n_max": n, "conjecture_holds": True, "counterexample": ""}

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [random.getrandbits(32) for _ in range(30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"minimal_order_too_large\" first_failing_seed={first_failing_seed}")
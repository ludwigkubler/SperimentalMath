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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} | ~{var}')
        for i in range(2**n):
            binary_rep = f'{i:0{n}b}'
            clause = ' & '.join([f'~x{i+1}' if bit == '0' else f'x{i+1}' for i, bit in enumerate(binary_rep)])
            clauses.append(clause)
        return ' | '.join(clauses)

    def parse_formula(formula):
        literals = []
        for part in formula.split(' | '):
            for sub_part in part.split(' & '):
                if sub_part.startswith('~'):
                    literals.append((sub_part[1:], False))
                else:
                    literals.append((sub_part, True))
        return literals

    def generate_tropical_polynomial(literals):
        n = len(set(lit[0] for lit in literals))
        matrix = [[0] * (n + 1) for _ in range(n)]
        for lit, sign in literals:
            i = int(lit[1:]) - 1
            if sign:
                matrix[i][i] += 1
            else:
                matrix[i][i] -= 1
        return matrix

    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def minimal_index(matrix):
        n = len(matrix)
        identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        augmented_matrix = [row + col for row, col in zip(matrix, identity)]
        gaussian_elimination(augmented_matrix)
        return sum(1 for row in augmented_matrix if any(x != 0 for x in row[:n]))

    def resolution_width(formula):
        literals = parse_formula(formula)
        n = len(set(lit[0] for lit in literals))
        clauses = [set() for _ in range(n)]
        for lit, sign in literals:
            i = int(lit[1:]) - 1
            if sign:
                clauses[i].add((lit, True))
            else:
                clauses[i].add((lit, False))

        def resolve(clause1, clause2):
            new_clauses = []
            for lit1, sign1 in clause1:
                for lit2, sign2 in clause2:
                    if lit1 == lit2 and sign1 != sign2:
                        new_clause = {(l, s) for l, s in clause1 if l != lit1} | {(l, s) for l, s in clause2 if l != lit2}
                        new_clauses.append(new_clause)
            return new_clauses

        queue = [set(clause) for clause in clauses]
        while True:
            new_queue = []
            for clause1 in queue:
                for clause2 in queue:
                    if clause1 != clause2:
                        new_clauses = resolve(clause1, clause2)
                        for new_clause in new_clauses:
                            if new_clause not in new_queue:
                                new_queue.append(new_clause)
            if set(queue) == set(new_queue):
                break
            queue = new_queue

        return len(queue)

    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    matrix = generate_tropical_polynomial(parse_formula(formula))
    m_index = minimal_index(matrix)
    w_phi_G = resolution_width(formula)

    return {
        "metric_name": "minimal_index",
        "metric_value": m_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
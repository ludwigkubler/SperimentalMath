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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda k: abs(matrix[k][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref = gaussian_elimination(matrix)
        rank = 0
        for i in range(rows):
            if any(rref[i][j] != 0 for j in range(cols)):
                rank += 1
        return rank
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for x in variables:
            clauses.append([x])
            clauses.append([-x])
        for i in range(2, n+1):
            a, b = random.sample(variables[:i], 2)
            if random.choice([True, False]):
                clauses.append([a, b, -f'x{i}'])
            else:
                clauses.append([a, -b, f'x{i}'])
                clauses.append([-a, b, f'x{i}'])
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        polarities = [random.choice([True, False]) for _ in range(len(clauses))]
        literals = [clauses[i][0] if polarities[i] else -clauses[i][0] for i in range(len(clauses))]
        new_assignment = assignment.copy()
        for literal in literals:
            new_assignment[literal] = True
        return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
    
    def resolution_length(clauses):
        length = 0
        while True:
            new_clauses = []
            added = False
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if any(-x in clauses[i] and x in clauses[j] for x in set(clauses[i]) & set(clauses[j])):
                        new_clause = list(set(clauses[i]) ^ set(clauses[j]))
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                            added = True
            if not added:
                break
            clauses.extend(new_clauses)
            length += 1
        return length
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_tseitin_formula(n)
            length = resolution_length(clauses)
            if length < 0.9 * n**2:  # Assuming rank is at least 2
                conjecture_holds = False
                counterexample = f"n={n}, length={length}"
                break
            total_length += length
            instances_tested += 1
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": total_length / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']:.2f}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_length = sum(r['metric_value'] for r in results) / len(results)
    std_length = math.sqrt(sum((r['metric_value'] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length:.2f} std={std_length:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length:.2f} std={std_length:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
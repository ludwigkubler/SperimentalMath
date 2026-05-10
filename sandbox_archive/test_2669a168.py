# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations, product

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def association_scheme(cnf):
    n = max(max(clause) for clause in cnf)
    adjacency_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                adjacency_matrix[literal][literal] += 1
            else:
                neg_literal = -literal
                adjacency_matrix[neg_literal][neg_literal] += 1
                for other_literal in clause:
                    if other_literal != literal and other_literal != -literal:
                        adjacency_matrix[abs(literal)][abs(other_literal)] += 1
    return adjacency_matrix

def laplacian(matrix):
    n = len(matrix)
    degree_vector = [sum(row) for row in matrix]
    laplacian_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                laplacian_matrix[i][j] = degree_vector[i]
            else:
                laplacian_matrix[i][j] = -matrix[i][j]
    return laplacian_matrix

def eigenvalues(matrix):
    n = len(matrix)
    if n == 1:
        return [matrix[0][0]]
    
    def determinant(submatrix):
        if len(submatrix) == 2:
            return submatrix[0][0] * submatrix[1][1] - submatrix[0][1] * submatrix[1][0]
        det = 0
        for j in range(len(submatrix)):
            det += (-1) ** j * submatrix[0][j] * determinant([row[:j] + row[j+1:] for row in submatrix[1:]])
        return det
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        else:
            char_poly = []
            for k in range(n, -1, -1):
                coeff = (-1) ** (n - k) * determinant([[matrix[i][j] for j in range(k, n)] for i in range(k, n)])
                char_poly.append(coeff)
            return char_poly
    
    def roots(poly):
        if len(poly) == 1:
            return []
        elif len(poly) == 2:
            a, b = poly
            return [-b / a]
        else:
            a, *coeffs = poly
            for r in range(-10, 11):  # Simple root finding
                if abs(sum(c * r**i for i, c in enumerate(coeffs))) < 1e-6:
                    roots.append(r)
                    break
            return roots
    
    char_poly = characteristic_polynomial(matrix)
    return roots(char_poly)

def dpll(cnf, assignment={}):
    unit_clauses = [c for c in cnf if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        polarity = True
        if literal < 0:
            polarity = False
            literal = -literal
        if literal in assignment and assignment[literal] != polarity:
            return False
        assignment[literal] = polarity
    pure_literals = [l for l, count in Counter(lit for clause in cnf for lit in clause).items() if count % 2 == 1]
    if pure_literals:
        literal = pure_literals[0]
        polarity = True
        if literal < 0:
            polarity = False
            literal = -literal
        if literal in assignment and assignment[literal] != polarity:
            return False
        assignment[literal] = polarity
    
    if not cnf:
        return True
    literals = [l for clause in cnf for l in clause]
    literal, polarity = random.choice(literals), True
    if literal < 0:
        polarity = False
        literal = -literal
    assignment[literal] = polarity
    new_cnf = []
    for clause in cnf:
        if not any(lit in assignment and assignment[lit] != (lit > 0) for lit in clause):
            new_clause = [l for l in clause if l != literal]
            if new_clause:
                new_cnf.append(new_clause)
    return dpll(new_cnf, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 4 * n)
    cnf = generate_cnf(n, m)
    assoc_scheme = association_scheme(cnf)
    laplacian_matrix = laplacian(assoc_scheme)
    eigenvals = eigenvalues(laplacian_matrix)
    smallest_eigenval = min(eigenvals, key=abs)
    if smallest_eigenval == 0:
        return {
            "metric_name": "product",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "smallest_eigenvalue_is_zero"
        }
    circuit_size = dpll(cnf)
    if circuit_size is None:
        return {
            "metric_name": "product",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_size_not_computable"
        }
    product = abs(smallest_eigenval) * circuit_size
    k = 0.5  # Empirical constant for the acceptance criterion
    return {
        "metric_name": "product",
        "metric_value": product,
        "instances_tested": 1,
        "conjecture_holds": product <= n**k,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = (sum((r['metric_value'] - mean)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        counterexample = next(r['counterexample'] for r in results if not r['conjecture_holds'])
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
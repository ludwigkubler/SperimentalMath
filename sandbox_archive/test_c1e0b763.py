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
    
    def generate_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clause.append(random.choice(['!', '']))
            clauses.append(' '.join(clause))
        return ' & '.join(clauses)

    def tseitin_formula(formula):
        literals = set()
        new_vars = {}
        for literal in formula.split():
            if literal[0] == '!':
                literals.add(literal[1:])
            else:
                literals.add(literal)
        
        next_var = 1
        for literal in literals:
            if literal not in new_vars:
                new_vars[literal] = f'y{next_var}'
                next_var += 1
        
        tseitin = []
        for clause in formula.split(' & '):
            if len(clause.split()) == 2:
                var, lit = clause.split()
                if lit[0] == '!':
                    tseitin.append(f'{new_vars[lit[1:]]} -> {var}')
                    tseitin.append(f'{lit[1:]} -> {new_vars[var]}')
                else:
                    tseitin.append(f'{new_vars[lit]} -> {var}')
                    tseitin.append(f'{lit} -> {new_vars[var]}')
            elif len(clause.split()) == 3 and clause[0] != '!':
                var, lit1, lit2 = clause.split()
                if lit1[0] == '!':
                    tseitin.append(f'{new_vars[lit1[1:]]} -> {var}')
                    tseitin.append(f'{lit1[1:]} -> {new_vars[var]}')
                else:
                    tseitin.append(f'{new_vars[lit1]} -> {var}')
                    tseitin.append(f'{lit1} -> {new_vars[var]}')
                
                if lit2[0] == '!':
                    tseitin.append(f'{new_vars[lit2[1:]]} -> {var}')
                    tseitin.append(f'{lit2[1:]} -> {new_vars[var]}')
                else:
                    tseitin.append(f'{new_vars[lit2]} -> {var}')
                    tseitin.append(f'{lit2} -> {new_vars[var]}')
        
        return ' & '.join(tseitin)

    def resolution_width(formula):
        clauses = formula.split(' & ')
        width = 0
        for clause in clauses:
            if len(clause.split()) == 3 and clause[0] != '!':
                width += 1
        return width

    def gaussian_elimination(matrix, b):
        n = len(matrix)
        augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
        
        for i in range(n):
            # Find the pivot
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            
            # Swap rows
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            # Eliminate below the pivot
            for j in range(i+1, n):
                factor = Fraction(augmented_matrix[j][i], augmented_matrix[i][i])
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        # Back-substitute
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = Fraction(augmented_matrix[i][n], augmented_matrix[i][i])
            for j in range(i+1, n):
                x[i] -= Fraction(augmented_matrix[i][j] * x[j], augmented_matrix[i][i])
        
        return x

    def clause_entanglement_graph(formula):
        literals = set()
        edges = []
        for literal in formula.split():
            if literal[0] == '!':
                literals.add(literal[1:])
            else:
                literals.add(literal)
        
        for literal in literals:
            for other_literal in literals:
                if literal != other_literal and literal not in other_literal and other_literal not in literal:
                    edges.append((literal, other_literal))
        
        return edges

    def quadratic_form(graph):
        n = len(graph)
        matrix = [[0] * n for _ in range(n)]
        b = [0] * n
        
        for i, (u, v) in enumerate(graph):
            u_idx = literals.index(u)
            v_idx = literals.index(v)
            matrix[u_idx][v_idx] += 1
            matrix[v_idx][u_idx] += 1
            b[u_idx] += 1
            b[v_idx] += 1
        
        x = gaussian_elimination(matrix, b)
        norm = sum(xi * xi for xi in x) ** 0.5
        return norm

    n_max = 40
    instances_tested = 30
    norm_values = []
    width_values = []

    for _ in range(instances_tested):
        n = random.randint(5, 40)
        formula = generate_formula(n)
        tseitin = tseitin_formula(formula)
        width = resolution_width(tseitin)
        graph = clause_entanglement_graph(tseitin)
        norm = quadratic_form(graph)

        norm_values.append(norm)
        width_values.append(width)

    correlation = pearson_correlation(norm_values, width_values)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

def pearson_correlation(x, y):
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
    var_x = sum((xi - mean_x) ** 2 for xi in x) / len(x)
    var_y = sum((yi - mean_y) ** 2 for yi in y) / len(y)
    
    if var_x == 0 or var_y == 0:
        return 0
    
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

def p_value(correlation, n):
    t_stat = correlation * math.sqrt((n - 2) / (1 - correlation ** 2))
    df = n - 2
    # Using cumulative distribution function of T-distribution to get p-value
    from scipy.stats import t
    p_value = 2 * (1 - t.cdf(abs(t_stat), df))
    return p_value

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
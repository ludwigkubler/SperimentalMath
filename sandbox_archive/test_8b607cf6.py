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
        literals = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, random.randint(1, len(literals)))
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def tseitin_formula(formula):
        literals = set()
        clauses = []
        new_vars = {}
        
        def add_clause(clause):
            if clause not in clauses:
                clauses.append(clause)
        
        for literal in formula.split():
            if literal.startswith('x'):
                literals.add(literal)
            elif literal == 'or':
                continue
            else:
                negated = literal.startswith('~')
                var = literal[1:] if negated else literal
                new_var = f'y{len(new_vars) + 1}'
                new_vars[var] = new_var
                add_clause(f'{new_var} {literal}')
                add_clause(f'~{new_var} ~{literal}')
        
        for literal in literals:
            new_var = f'y{len(new_vars) + 1}'
            new_vars[literal] = new_var
            add_clause(f'{new_var} ~{literal}')
            add_clause(f'~{new_var} {literal}')
        
        return ' and '.join(clauses), new_vars
    
    def clause_entanglement_graph(formula):
        graph = {}
        for literal in formula.split():
            if literal.startswith('x'):
                var = literal
            elif literal == 'or':
                continue
            else:
                negated = literal.startswith('~')
                var = literal[1:] if negated else literal
        
        for clause in formula.split(' and '):
            literals = clause.split(' or ')
            for i, lit1 in enumerate(literals):
                for j, lit2 in enumerate(literals):
                    if i < j:
                        if (lit1, lit2) not in graph:
                            graph[(lit1, lit2)] = 0
                        graph[(lit1, lit2)] += 1
        
        return graph
    
    def quadratic_form(graph):
        n = len(graph)
        Q = [[0] * n for _ in range(n)]
        
        for (i, j), count in graph.items():
            idx_i = literals.index(i) if i.startswith('x') else new_vars[i]
            idx_j = literals.index(j) if j.startswith('x') else new_vars[j]
            Q[idx_i][idx_j] += count
            Q[idx_j][idx_i] += count
        
        return Q
    
    def resolution_width(formula):
        stack = []
        for clause in formula.split(' and '):
            stack.append(clause)
        
        while len(stack) > 1:
            clause1 = stack.pop()
            clause2 = stack.pop()
            
            new_clauses = []
            for lit1 in clause1.split(' or '):
                if lit1.startswith('~'):
                    negated_lit1 = lit1[1:]
                else:
                    negated_lit1 = '~' + lit1
                
                for lit2 in clause2.split(' or '):
                    if lit2 == negated_lit1:
                        continue
                    new_clause = list(set(clause1.split(' or ') + clause2.split(' or ')) - {lit1, lit2})
                    new_clauses.append(' or '.join(new_clause))
            
            stack.extend(new_clauses)
        
        return len(stack[0].split(' or '))
    
    def matrix_norm(Q):
        n = len(Q)
        max_row_sum = 0
        for row in Q:
            row_sum = sum(abs(x) for x in row)
            if row_sum > max_row_sum:
                max_row_sum = row_sum
        
        return max_row_sum
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, 41):
        formula = generate_formula(n)
        tseitin, new_vars = tseitin_formula(formula)
        graph = clause_entanglement_graph(tseitin)
        Q = quadratic_form(graph)
        width = resolution_width(tseitin)
        
        norm = matrix_norm(Q)
        metric_values.append((norm, width))
        instances_tested += n
    
    if not metric_values:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    norm_values, width_values = zip(*metric_values)
    mean_norm = sum(norm_values) / len(norm_values)
    mean_width = sum(width_values) / len(width_values)
    
    if instances_tested < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    if n_max < 16:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    correlation = pearson_correlation(norm_values, width_values)
    p_value = calculate_p_value(correlation, len(norm_values) - 2)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

def pearson_correlation(x, y):
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
    var_x = sum((xi - mean_x) ** 2 for xi in x) / len(x)
    var_y = sum((yi - mean_y) ** 2 for yi in y) / len(y)
    
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

def calculate_p_value(r, n):
    t_statistic = r * math.sqrt(n - 2) / math.sqrt(1 - r**2)
    degrees_of_freedom = n - 2
    p_value = 2 * (1 - math.erf(abs(t_statistic) / math.sqrt(2)))
    
    return p_value

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
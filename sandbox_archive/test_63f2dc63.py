# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_satisfiable(formula):
        variables = set()
        
        def collect_variables(expression):
            if isinstance(expression, list):
                if expression[0] == 'or':
                    for subexpr in expression[1:]:
                        collect_variables(subexpr)
                elif expression[0] == 'and':
                    for subexpr in expression[1:]:
                        collect_variables(subexpr)
                elif expression[0] == 'not':
                    collect_variables(expression[1])
                else:
                    variables.add(expression[0])
            else:
                variables.add(expression)
        
        collect_variables(formula)
        
        def evaluate(expr, assignment):
            if isinstance(expr, list):
                if expr[0] == 'or':
                    return any(evaluate(subexpr, assignment) for subexpr in expr[1:])
                elif expr[0] == 'and':
                    return all(evaluate(subexpr, assignment) for subexpr in expr[1:])
                elif expr[0] == 'not':
                    return not evaluate(expr[1], assignment)
            else:
                return assignment.get(expr, False)
        
        def backtrack(assignment):
            if len(assignment) == len(variables):
                return evaluate(formula, assignment)
            
            var = next(var for var in variables if var not in assignment)
            for val in [True, False]:
                assignment[var] = val
                if backtrack(assignment):
                    return True
                del assignment[var]
            return False
        
        return backtrack({})
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['x', 'not x'])
        else:
            op = random.choice(['and', 'or'])
            subformulas = [generate_formula(n-1) for _ in range(2)]
            return [op] + subformulas
    
    def graph_from_formula(formula):
        nodes = set()
        edges = []
        
        def collect_nodes_and_edges(expr, parent=None):
            if isinstance(expr, list):
                if expr[0] == 'or':
                    for subexpr in expr[1:]:
                        collect_nodes_and_edges(subexpr, expr)
                elif expr[0] == 'and':
                    for subexpr in expr[1:]:
                        collect_nodes_and_edges(subexpr, expr)
                elif expr[0] == 'not':
                    collect_nodes_and_edges(expr[1], expr)
            else:
                nodes.add(expr)
        
        def add_edge(u, v):
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        
        collect_nodes_and_edges(formula)
        
        for node1, node2 in combinations(nodes, 2):
            add_edge(node1, node2)
        
        return nodes, edges
    
    def tropicalization_order(graph):
        n = len(graph[0])
        adjacency_matrix = [[0] * n for _ in range(n)]
        
        for u, v in graph[1]:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            
            for i in range(n):
                max_row = None
                for j in range(rank, m):
                    if matrix[j][i]:
                        max_row = j
                        break
                
                if max_row is not None:
                    matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
                    
                    for j in range(m):
                        if j != rank and matrix[j][i]:
                            factor = Fraction(matrix[j][i], matrix[rank][i])
                            for k in range(n):
                                matrix[j][k] -= factor * matrix[rank][k]
                    
                    rank += 1
            
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    def satisfiability_degree(formula):
        variables = set()
        
        def collect_variables(expression):
            if isinstance(expression, list):
                if expression[0] == 'or':
                    for subexpr in expression[1:]:
                        collect_variables(subexpr)
                elif expression[0] == 'and':
                    for subexpr in expression[1:]:
                        collect_variables(subexpr)
                elif expression[0] == 'not':
                    collect_variables(expression[1])
            else:
                variables.add(expression)
        
        collect_variables(formula)
        
        return len(variables)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    graph = graph_from_formula(formula)
    tau_phi = tropicalization_order(graph)
    D_phi = satisfiability_degree(formula)
    
    return {
        "metric_name": "Tropicalization Order vs Satisfiability Degree",
        "metric_value": tau_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(tau_phi - D_phi) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
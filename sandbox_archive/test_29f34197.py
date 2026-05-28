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
    
    def tseitin_formula(n):
        if n < 2:
            return [], []
        
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Create OR clauses
        for i in range(1, n+1):
            clause = [variables[i-1]]
            for j in range(i):
                clause.append(f'~{variables[j]}')
            clauses.append(clause)
        
        # Create AND clauses
        for i in range(n):
            for j in range(i+1, n):
                clauses.append([f'~{variables[i]}', f'~{variables[j]}', variables[i+j]])
        
        return variables, clauses
    
    def graph_from_clauses(clauses):
        graph = {}
        for clause in clauses:
            for literal in clause:
                if literal.startswith('~'):
                    var = literal[1:]
                else:
                    var = literal
                if var not in graph:
                    graph[var] = set()
                for other_var in clause:
                    if other_var != literal and other_var not in graph[var]:
                        graph[var].add(other_var)
        return graph
    
    def min_rank(graph):
        n = len(graph)
        matrix = [[0]*n for _ in range(n)]
        
        # Create adjacency matrix
        for i, neighbors in enumerate(graph.values()):
            for neighbor in neighbors:
                j = variables.index(neighbor)
                matrix[i][j] = 1
        
        # Gaussian elimination to find rank
        rank = n
        for i in range(n):
            if matrix[i][i] == 0:
                found_pivot = False
                for j in range(i+1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    rank -= 1
                    continue
            
            # Eliminate other rows
            for j in range(n):
                if i == j:
                    continue
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        return rank
    
    def resolution_length(clauses, variables):
        stack = []
        seen = set()
        
        def resolve(l1, l2):
            if l1.startswith('~'):
                var1 = l1[1:]
            else:
                var1 = l1
            if l2.startswith('~'):
                var2 = l2[1:]
            else:
                var2 = l2
            
            if var1 == var2:
                return None
            elif var1 in seen or var2 in seen:
                return None
            else:
                seen.add(var1)
                seen.add(var2)
                stack.append(l1)
                stack.append(l2)
                return len(stack)
        
        for clause in clauses:
            if not any(l.startswith('~') and l[1:] in variables for l in clause):
                continue
            
            for literal in clause:
                if literal.startswith('~'):
                    var = literal[1:]
                else:
                    var = literal
                
                if var in seen:
                    continue
                
                found_resolvent = False
                for other_clause in clauses:
                    if any(l.startswith('~') and l[1:] == var for l in other_clause):
                        resolvent_length = resolve(literal, f'~{var}')
                        if resolvent_length is not None:
                            return resolvent_length
                        found_resolvent = True
                
                if not found_resolvent:
                    return 1
        
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        graph = graph_from_clauses(clauses)
        ν_G = min_rank(graph)
        
        if ν_G == 0:
            return {
                "metric_name": "resolution_length",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        length = resolution_length(clauses, variables)
        results.append((ν_G, length))
    
    if not results:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    ν_G_values = [ν for ν, _ in results]
    lengths = [length for _, length in results]
    
    def spearman_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i+1 for i in range(n)}
        rank_y = {y[i]: i+1 for i in range(n)}
        
        sum_d_squared = sum((rank_x[x[i]] - rank_y[y[i]])**2 for i in range(n))
        return 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    
    correlation = spearman_correlation(ν_G_values, lengths)
    
    return {
        "metric_name": "spearman_correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r >= 0.95) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        elif any(r < 0.95 for r in results):
            first_failing_seed = seeds[results.index(min(r for r in results if r < 0.95))]
            print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")
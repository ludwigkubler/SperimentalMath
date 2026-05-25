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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        
        for i in range(n):
            if matrix[rank][i] == 0:
                found_non_zero = False
                for j in range(rank + 1, n):
                    if matrix[j][i] != 0:
                        matrix[rank], matrix[j] = matrix[j], matrix[rank]
                        found_non_zero = True
                        break
                if not found_non_zero:
                    continue
            
            factor = Fraction(-matrix[j][i], matrix[rank][i])
            for k in range(n):
                matrix[j][k] += factor * matrix[rank][k]
            
            rank += 1
        
        return rank
    
    def tseitin_formula(n, delta):
        variables = list(range(1, n + 1))
        clauses = []
        
        # Generate literals
        literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n * delta + 1)]
        
        # Create clauses
        for literal in literals:
            if literal[0] == '-':
                clause = [literal]
            else:
                clause = [-literal, random.choice(literals), random.choice(literals)]
            
            clauses.append(clause)
        
        return variables, clauses
    
    def graph_from_formula(variables, clauses):
        n = len(variables)
        adj_matrix = [[0] * (2 * n) for _ in range(2 * n)]
        
        for i, var in enumerate(variables):
            adj_matrix[i][n + i] = 1
            adj_matrix[n + i][i] = 1
        
        for clause in clauses:
            if len(clause) == 1:
                literal = clause[0]
                if literal[0] == '-':
                    var = int(literal[1:])
                    adj_matrix[var - 1][n + var - 1] = 1
                else:
                    var = int(literal)
                    adj_matrix[n + var - 1][var - 1] = 1
            elif len(clause) == 2:
                literal1, literal2 = clause
                if literal1[0] == '-':
                    var1 = int(literal1[1:])
                else:
                    var1 = int(literal1)
                
                if literal2[0] == '-':
                    var2 = int(literal2[1:])
                else:
                    var2 = int(literal2)
                
                adj_matrix[var1 - 1][n + var2 - 1] = 1
                adj_matrix[n + var2 - 1][var1 - 1] = 1
                adj_matrix[var2 - 1][n + var1 - 1] = 1
                adj_matrix[n + var1 - 1][var2 - 1] = 1
        
        return adj_matrix
    
    def resolution_length(clauses):
        stack = clauses[:]
        visited = set()
        
        while stack:
            clause = stack.pop(0)
            if len(clause) == 1:
                literal = clause[0]
                if literal[0] == '-':
                    var = int(literal[1:])
                else:
                    var = int(literal)
                
                if -var in visited:
                    return float('inf')
                visited.add(var)
            elif len(clause) == 2:
                literal1, literal2 = clause
                if literal1[0] == '-':
                    var1 = int(literal1[1:])
                else:
                    var1 = int(literal1)
                
                if literal2[0] == '-':
                    var2 = int(literal2[1:])
                else:
                    var2 = int(literal2)
                
                if -var1 in visited and not var2 in visited:
                    stack.append([-literal2])
                elif -var2 in visited and not var1 in visited:
                    stack.append([-literal1])
        
        return len(visited)
    
    n = random.randint(5, 40)
    delta = random.randint(1, 5)
    variables, clauses = tseitin_formula(n, delta)
    graph = graph_from_formula(variables, clauses)
    rank = gaussian_elimination(graph)
    length = resolution_length(clauses)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= 2 ** (math.log(n / delta, 2) ** 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((r['metric_value'] - mean_rank) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
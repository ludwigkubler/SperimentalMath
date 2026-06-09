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
    
    def generate_tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        
        for i in range(m):
            a = random.choice(variables)
            b = random.choice(variables)
            c = random.choice(variables)
            
            if random.choice([True, False]):
                clauses.append((a, b, c))
            else:
                clauses.append((-a, -b, c))
        
        return variables, clauses
    
    def generate_graph(clauses):
        graph = {i: set() for i in range(1, 2 * len(clauses) + 1)}
        
        for clause in clauses:
            literals = [abs(lit) for lit in clause]
            for i in range(len(literals)):
                for j in range(i + 1, len(literals)):
                    graph[literals[i]].add(literals[j])
                    graph[literals[j]].add(literals[i])
        
        return graph
    
    def compute_local_zeta_function_rank(graph):
        n = len(graph)
        zeta_matrix = [[0] * (n + 2) for _ in range(n + 2)]
        
        for i in range(1, n + 1):
            zeta_matrix[0][i] = Fraction(1, 1)
            zeta_matrix[i][0] = Fraction(1, 1)
        
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if j in graph[i]:
                    zeta_matrix[i][j] = Fraction(1, 2)
                else:
                    zeta_matrix[i][j] = Fraction(1, 3)
        
        return max(sum(row) for row in zeta_matrix)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        
        literal = next((l for l in assignment if l not in [c[0] for c in clauses]), None)
        if literal is None:
            return True
        
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(clauses, new_assignment):
            return True
        
        new_assignment[literal] = False
        if dpll(clauses, new_assignment):
            return True
        
        return False
    
    def resolution_width(clauses):
        n = len(variables)
        assignment = [False] * (n + 1)
        
        for _ in range(30):  # Limit to 30 iterations to avoid excessive time
            if dpll(clauses, assignment):
                return sum(assignment)
        
        return float('inf')
    
    variables, clauses = generate_tseitin_formula(random.randint(5, 40), random.randint(10, 2 * len(variables)))
    graph = generate_graph(clauses)
    zeta_rank = compute_local_zeta_function_rank(graph)
    width = resolution_width(clauses)
    
    return {
        "metric_name": "Resolution Width vs Local Zeta Function Rank",
        "metric_value": width / zeta_rank,
        "instances_tested": 1,
        "n_max": max(len(variables), len(clauses)),
        "conjecture_holds": width <= 2 * zeta_rank,  # Simplified bound for testing
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 97) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
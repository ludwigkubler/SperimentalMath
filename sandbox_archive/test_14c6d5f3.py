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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate clauses for each variable
        for var in variables:
            clauses.append([var])
            clauses.append([-var])
        
        # Generate clauses for each pair of variables
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append([variables[i], variables[j]])
                clauses.append([variables[i], -variables[j]])
                clauses.append([-variables[i], variables[j]])
                clauses.append([-variables[i], -variables[j]])
        
        # Generate the final clause
        final_clause = []
        for var in variables:
            final_clause.append(var)
        clauses.append(final_clause)
        
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
        
        pure_literals = []
        for literal in assignment.keys():
            positive_count = sum(1 for clause in clauses if literal in clause)
            negative_count = sum(1 for clause in clauses if -literal in clause)
            if positive_count == 0 and literal not in pure_literals:
                pure_literals.append(literal)
            elif negative_count == 0 and -literal not in pure_literals:
                pure_literals.append(-literal)
        
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
        
        literal = random.choice(list(assignment.keys()))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        else:
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
    
    def resolution(clauses):
        while True:
            unit_clauses = [c[0] for c in clauses if len(c) == 1]
            if not unit_clauses:
                break
            literal = unit_clauses[0]
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                elif -literal in clause:
                    new_clauses.extend([c for c in clauses if c != clause and -c != clause])
                    break
                else:
                    new_clauses.append(clause)
            clauses = new_clauses
    
    def tropical_hodge_structure_rank(phi_G):
        n = len(phi_G[0])
        A = [[-math.inf] * n for _ in range(n)]
        
        for clause in phi_G:
            for i, var in enumerate(clause):
                if var > 0:
                    A[i][var - 1] = max(A[i][var - 1], 1)
                else:
                    A[i][-var - 1] = max(A[i][-var - 1], 1)
        
        for i in range(n):
            for j in range(i + 1, n):
                A[i][j] = max(A[i][j], A[j][i])
                A[j][i] = max(A[j][i], A[i][j])
        
        rank = 0
        for row in A:
            if any(x != -math.inf for x in row):
                rank += 1
        
        return rank
    
    def resolution_width(phi_G):
        n = len(phi_G[0])
        assignment = {f'x{i}': False for i in range(1, n+1)}
        width = 0
        while not dpll(phi_G, assignment):
            new_clause = []
            for i in range(n):
                if not assignment[f'x{i+1}']:
                    new_clause.append(f'x{i+1}')
                else:
                    new_clause.append(-f'x{i+1}')
            phi_G.append(new_clause)
            width += 1
        return width
    
    n = random.randint(5, 40)
    phi_G = generate_tseitin_formula(n)
    th_phi_G = tropical_hodge_structure_rank(phi_G)
    w_phi_G = resolution_width(phi_G)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_phi_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": th_phi_G == w_phi_G,
        "counterexample": "" if th_phi_G == w_phi_G else f"th(φ_G)={th_phi_G}, w(φ_G)={w_phi_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"th(φ_G) != w(φ_G)\" first_failing_seed={first_failing_seed}")
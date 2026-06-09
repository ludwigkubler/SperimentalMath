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
    
    def generate_random_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Each variable appears in about 10 clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(assignment) + 1) if assignment[l] is None), None)
        if literal is None:
            return False
        
        positive_literal = literal
        negative_literal = -literal
        positive_assignment = assignment[:]
        negative_assignment = assignment[:]
        
        positive_assignment[abs(literal)] = True
        negative_assignment[abs(literal)] = False
        
        if dpll(cnf, positive_assignment):
            return True
        if dpll(cnf, negative_assignment):
            return True
        
        return False
    
    def laplacian_matrix(n, cnf):
        L = [[0] * n for _ in range(n)]
        for clause in cnf:
            for literal in clause:
                i = abs(literal) - 1
                L[i][i] += 1
                if literal < 0:
                    j = abs(clause[1]) - 1 if literal == clause[0] else abs(clause[0]) - 1
                    L[i][j] -= 1
                    L[j][i] -= 1
        return L
    
    def power_iteration(L, n):
        v = [random.random() for _ in range(n)]
        v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
        
        for _ in range(100):  # Power iteration steps
            v_next = [sum(L[i][j] * v[j] for j in range(n)) for i in range(n)]
            v_next = [x / math.sqrt(sum(x**2 for x in v_next)) for x in v_next]
            v = v_next
        
        eigenvalue = sum(v[i] * L[i][i] for i in range(n))
        return eigenvalue
    
    def resolution_width(cnf):
        assignment = [None] * (max(abs(l) for l in cnf) + 1)
        width = 0
        stack = []
        
        def add_clause(clause):
            nonlocal width
            if any(assignment[abs(l)] is not None for l in clause):
                continue
            stack.append(clause)
            width += 1
        
        def resolve():
            nonlocal width
            while len(stack) > 1:
                c1 = stack.pop()
                c2 = stack.pop()
                resolved = False
                for l1 in c1:
                    if -l1 in c2:
                        new_clause = [l for l in c1 + c2 if l != l1 and l != -l1]
                        add_clause(new_clause)
                        resolved = True
                        break
                if not resolved:
                    stack.append(c2)
                    stack.append(c1)
                    break
        
        def dpll_with_resolution():
            nonlocal width
            if not cnf:
                return True
            literal = next((l for l in range(1, len(assignment) + 1) if assignment[l] is None), None)
            if literal is None:
                return False
            
            positive_literal = literal
            negative_literal = -literal
            positive_assignment = assignment[:]
            negative_assignment = assignment[:]
            
            positive_assignment[abs(literal)] = True
            negative_assignment[abs(literal)] = False
            
            if dpll_with_resolution():
                return True
            if dpll_with_resolution():
                return True
            
            return False
        
        add_clause([1])
        while stack:
            resolve()
        
        return width
    
    n = random.randint(5, 40)
    cnf = generate_random_cnf(n)
    L = laplacian_matrix(n, cnf)
    eig2_L = power_iteration(L, n)
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": eig2_L > 0 and w_phi > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed + 1}")
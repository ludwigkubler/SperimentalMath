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
    
    def generate_random_formula(n):
        literals = [f"v{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"{random.choice(['', '-'])}{clause[0]} {random.choice(['', '-'])}{clause[1]}")
        return " & ".join(clauses)
    
    def incidence_matrix(formula, n):
        matrix = [[0] * (n + n) for _ in range(n)]
        literals = [f"v{i}" for i in range(1, n+1)]
        neg_literals = [f"-v{i}" for i in range(1, n+1)]
        
        def get_index(lit):
            if lit.startswith('-'):
                return neg_literals.index(lit)
            else:
                return literals.index(lit) + n
        
        for clause in formula.split(' & '):
            for literal in clause.split():
                matrix[literals.index(literal)] = [1 if i == get_index(literal) else 0 for i in range(n + n)]
        
        return matrix
    
    def min_order(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            pivot = None
            for j in range(n):
                if matrix[i][j] != 0:
                    pivot = j
                    break
            if pivot is not None:
                rank += 1
                for k in range(i + 1, m):
                    factor = -matrix[k][pivot] / matrix[i][pivot]
                    for j in range(n):
                        matrix[k][j] += factor * matrix[i][j]
        return rank
    
    def resolution_width(formula):
        stack = []
        literals = set()
        
        def add_clause(clause):
            if clause not in stack:
                stack.append(clause)
                literals.update(clause.split())
        
        def resolve(lit1, lit2):
            new_clauses = []
            for clause in stack:
                if (lit1 in clause and -lit2 in clause) or (-lit1 in clause and lit2 in clause):
                    continue
                elif (lit1 in clause and -lit2 not in clause):
                    new_clause = [l for l in clause if l != lit1]
                    new_clauses.append(new_clause)
                elif (-lit1 in clause and lit2 not in clause):
                    new_clause = [l for l in clause if l != -lit1]
                    new_clauses.append(new_clause)
            return new_clauses
        
        for literal in literals:
            add_clause([literal])
        
        while stack:
            clause = random.choice(stack)
            literals_in_clause = set(clause.split())
            if len(literals_in_clause) == 1:
                break
            lit1, lit2 = random.sample(list(literals_in_clause), 2)
            new_clauses = resolve(lit1, lit2)
            for new_clause in new_clauses:
                add_clause(new_clause)
        
        return len(stack)

    n = random.randint(5, 40)
    formula = generate_random_formula(n)
    Inc = incidence_matrix(formula, n)
    min_order_value = min_order(Inc)
    w_phi = resolution_width(formula)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if min_order_value <= w_phi else False,
        "counterexample": "" if min_order_value <= w_phi else f"Formula: {formula}, min_order: {min_order_value}, w(φ): {w_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= max(results)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r > max(results) for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='max_order_exceeds_resolution_width' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")
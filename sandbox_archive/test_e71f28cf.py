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
    
    def tseitin_polynomial(literals, clauses):
        n = len(literals)
        p = {lit: 0 for lit in literals}
        for clause in clauses:
            if len(clause) == 1:
                p[clause[0]] += 1
            else:
                new_var = f'x{n + 1}'
                n += 1
                p[new_var] = 0
                for lit in clause:
                    p[lit] -= 1
                    p[f'{lit} OR {new_var}'] += 1
                p[f'{new_var} OR ~{new_var}'] += 1
        return p
    
    def resolution(literals, clauses):
        n = len(literals)
        while True:
            new_clauses = []
            for i in range(n):
                for j in range(i + 1, n):
                    lit_i = literals[i]
                    lit_j = literals[j]
                    if f'{lit_i} OR {lit_j}' in clauses and f'~{lit_i} OR ~{lit_j}' in clauses:
                        new_lit = f'{lit_i} AND {lit_j}'
                        if new_lit not in literals:
                            literals.append(new_lit)
                            n += 1
                        for clause in clauses:
                            if lit_i in clause:
                                new_clauses.append([new_lit] + [x for x in clause if x != lit_i])
                            elif lit_j in clause:
                                new_clauses.append([new_lit] + [x for x in clause if x != lit_j])
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    def tropical_derivative_rank(p):
        n = len(p)
        jacobian = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    lit_i = literals[i]
                    lit_j = literals[j]
                    if f'{lit_i} OR {lit_j}' in p and f'~{lit_i} OR ~{lit_j}' in p:
                        jacobian[i][j] = 1
        rank = 0
        for row in jacobian:
            if any(row):
                rank += 1
        return rank
    
    def generate_formula(n, clause_density):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(int(clause_density * n)):
            clause = random.sample(literals, random.randint(1, n))
            if all(f'{lit} OR {other_lit}' not in clauses and f'~{lit} OR ~{other_lit}' not in clauses for other_lit in literals):
                clauses.append(clause)
        return literals, clauses
    
    def solve(lits_true, cls):
        stack = []
        while lits_true:
            lit = lits_true.pop()
            if lit in cls:
                continue
            if f'~{lit}' in cls:
                return False
            for clause in cls:
                if lit in clause and any(other_lit not in lits_true and other_lit != f'~{lit}' for other_lit in clause):
                    break
            else:
                stack.append(lit)
        while stack:
            lit = stack.pop()
            for clause in cls:
                if lit in clause:
                    cls.remove(clause)
                    for other_lit in clause:
                        if other_lit == f'~{lit}':
                            continue
                        if other_lit not in lits_true and other_lit != lit:
                            lits_true.add(other_lit)
        return True
    
    n = 5
    while n <= 40:
        literals, clauses = generate_formula(n, 2 / n)
        p = tseitin_polynomial(literals, clauses)
        mtr = tropical_derivative_rank(p)
        w = resolution(literals, clauses)
        
        if mtr == 0 or w == 0:
            continue
        
        yield {"mtr": mtr, "w": w}
    
    return {
        "metric_name": "correlation",
        "metric_value": sum(x["mtr"] * x["w"] for x in results) / sum(x["mtr"] ** 2 for x in results),
        "instances_tested": len(results),
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {seed=}, {trial_result}")
        results.extend(trial_result)
    
    mean_mtr = sum(x["mtr"] for x in results) / len(results)
    std_mtr = math.sqrt(sum((x["mtr"] - mean_mtr) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["mtr"] >= 0.8 * x["w"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mtr} std={std_mtr} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")
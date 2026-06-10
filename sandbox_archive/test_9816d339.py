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
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            if literal < 0:
                literal = -literal
                assignment.append(-literal)
            else:
                assignment.append(literal)
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            return dpll(new_cnf, assignment)
        pure_literals = {}
        for clause in cnf:
            pos_literals = set([l for l in clause if l > 0])
            neg_literals = set([-l for l in clause if l < 0])
            if len(pos_literals) == 1:
                literal = list(pos_literals)[0]
                pure_literals[literal] = True
            elif len(neg_literals) == 1:
                literal = -list(neg_literals)[0]
                pure_literals[literal] = False
        for literal, polarity in pure_literals.items():
            if polarity:
                assignment.append(literal)
            else:
                assignment.append(-literal)
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if not dpll(new_cnf, assignment):
                return False
        for literal in range(1, n+1):
            if literal not in assignment and -literal not in assignment:
                new_assignment = assignment + [literal]
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                if dpll(new_cnf, new_assignment):
                    return True
                new_assignment = assignment + [-literal]
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                if dpll(new_cnf, new_assignment):
                    return True
        return False
    
    def generate_cnf(n, m):
        cnf = []
        variables = set(range(1, n+1))
        while len(cnf) < m:
            clause = random.sample(variables, 2)
            if clause not in cnf and -clause[0] not in cnf and -clause[1] not in cnf:
                cnf.append(clause)
        return cnf
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(1, min(n * (n - 1) // 2, 10))
    cnf = generate_cnf(n, m)
    
    def polynomial(cnf):
        poly = {}
        for clause in cnf:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= literal
                else:
                    term /= -literal
            if term not in poly:
                poly[term] = 0
            poly[term] += 1
        return poly
    
    def tropical_motivic_rank(poly):
        rank = 0
        for term, coeff in poly.items():
            rank = max(rank, sum(math.log2(abs(coeff)), math.log2(abs(term))))
        return rank
    
    def degree(clause):
        return sum(1 if literal > 0 else -1 for literal in clause)
    
    def num_satisfying_assignments(cnf):
        assignment = [False] * (n + 1)
        count = 0
        while True:
            valid = True
            for clause in cnf:
                if all(not assignment[abs(literal)] == (literal > 0) for literal in clause):
                    valid = False
                    break
            if valid:
                count += 1
            if not dpll(cnf, assignment):
                break
            assignment[random.choice(range(1, n+1))] = not assignment[random.choice(range(1, n+1))]
        return count
    
    poly = polynomial(cnf)
    mtr = tropical_motivic_rank(poly)
    max_degree = max(degree(clause) for clause in cnf)
    min_satisfying_assignments = num_satisfying_assignments(cnf)
    
    metric_value = mtr
    instances_tested = 1
    n_max = n
    conjecture_holds = mtr >= max_degree + min_satisfying_assignments
    counterexample = "" if conjecture_holds else f"mtr({mtr}) < {max_degree} + {min_satisfying_assignments}"
    
    return {
        "metric_name": "tropical_motivic_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
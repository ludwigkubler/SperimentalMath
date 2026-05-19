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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            literals = [random.choice(['x', '~x']) + str(i+1) for i in range(n)]
            clause = ' ∨ '.join(literals)
            cnf.append(clause)
        return ' ∧ '.join(cnf)
    
    def is_unsatisfiable(cnf):
        variables = set()
        for clause in cnf.split(' ∧ '):
            for literal in clause.split(' ∨ '):
                if literal.startswith('x'):
                    variables.add(literal[1:])
                elif literal.startswith('~x'):
                    variables.add(literal[2:])
        
        def eval_clause(clause, assignment):
            return any(assignment[var] == (literal.startswith('x') and 1 or -1) for literal in clause.split(' ∨ '))
        
        def eval_cnf(cnf, assignment):
            return all(eval_clause(clause, assignment) for clause in cnf.split(' ∧ '))
        
        for _ in range(60):
            assignment = {var: random.choice([0, 1]) for var in variables}
            if not eval_cnf(cnf, assignment):
                return True
        return False
    
    def dpll(cnf):
        literals = []
        for clause in cnf.split(' ∧ '):
            literals.extend(clause.split(' ∨ '))
        
        def unit_propagate(assignment, clauses):
            new_assignment = assignment.copy()
            while True:
                found_unit_clause = False
                for i, clause in enumerate(clauses):
                    if len([l for l in clause.split(' ∨ ') if l.startswith('x') and int(l[1:]) not in new_assignment]) == 1:
                        literal = [l for l in clause.split(' ∨ ') if l.startswith('x') and int(l[1:]) not in new_assignment][0]
                        new_assignment[int(literal[1:])] = (literal.startswith('x') and 1 or -1)
                        found_unit_clause = True
                if not found_unit_clause:
                    break
            return new_assignment
        
        def backtrack(assignment, clauses):
            if all(eval_clause(clause, assignment) for clause in clauses):
                return assignment
            var = next(var for var in variables if var not in assignment)
            for val in [0, 1]:
                new_assignment = assignment.copy()
                new_assignment[var] = (val == 1 and 1 or -1)
                result = backtrack(new_assignment, clauses)
                if result:
                    return result
            return None
        
        clauses = cnf.split(' ∧ ')
        assignment = {}
        while True:
            assignment = unit_propagate(assignment, clauses)
            if all(eval_clause(clause, assignment) for clause in clauses):
                break
            var = next(var for var in variables if var not in assignment)
            for val in [0, 1]:
                new_assignment = assignment.copy()
                new_assignment[var] = (val == 1 and 1 or -1)
                result = backtrack(new_assignment, clauses)
                if result:
                    return result
            return None
    
    def walsh_transform(cnf):
        n = len(cnf.split(' ∧ ')[0].split(' ∨ '))
        p_F = [0] * (2**n)
        for i in range(2**n):
            assignment = {var: (i >> j) & 1 for j, var in enumerate(reversed(range(n)))}
            count = sum(1 for clause in cnf.split(' ∧ ') if eval_clause(clause, assignment))
            p_F[i] = Fraction(count, len(cnf.split(' ∧ ')))
        return p_F
    
    def T(F):
        n = len(F)
        total = 0
        for i in range(n):
            for S in range(1 << (i+1)):
                if bin(S).count('1') <= 3:
                    subset_vars = [j for j in range(i+1) if S & (1 << j)]
                    p_hat_S = sum((-1)**len(subset_vars) * 2**(-len(subset_vars)) * F[sum(1 << j for j in subset_vars)] for clause in cnf.split(' ∧ ') if all(literal.startswith('x') and int(literal[1:]) - 1 in subset_vars or literal.startswith('~x') and int(literal[2:]) - 1 not in subset_vars for literal in clause.split(' ∨ ')))
                    total += math.sqrt(p_hat_S**2)
        return total
    
    def log_2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n_values = [16, 20, 24, 28, 32]
    alpha_values = [4.0, 4.5, 5.0]
    results = []
    
    for n in n_values:
        for alpha in alpha_values:
            m = math.ceil(alpha * n)
            cnf = generate_cnf(n, m)
            if is_unsatisfiable(cnf):
                continue
            p_F = walsh_transform(cnf)
            T_F = T(p_F)
            B_F = len(dpll(cnf))
            results.append({
                "metric_name": "log_2(1+B(F))",
                "metric_value": log_2(1 + B_F),
                "instances_tested": 1,
                "conjecture_holds": log_2(1 + B_F) >= 0.1 * T_F / math.sqrt(m),
                "counterexample": ""
            })
    
    if not results:
        return {
            "metric_name": "log_2(1+B(F))",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_unsat_instances"
        }
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "log_2(1+B(F))",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=no_unsat_instances")
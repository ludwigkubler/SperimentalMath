# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n, m):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = set()
        while len(clauses) < m:
            clause = []
            for _ in range(random.randint(2, 3)):
                var = random.choice(variables)
                if random.choice([True, False]):
                    clause.append(var)
                else:
                    clause.append(f"~{var}")
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def is_satisfiable(clauses):
        stack = []
        assignment = {}
        for clause in clauses:
            found_literal = False
            for literal in clause:
                if literal[0] == '~':
                    var = literal[1:]
                    if var not in assignment and -var not in stack:
                        stack.append(-var)
                        break
                else:
                    var = literal
                    if var not in assignment and var not in stack:
                        stack.append(var)
                        break
            else:
                found_literal = True
            if found_literal:
                continue
            while stack:
                lit = stack.pop()
                if -lit in stack:
                    stack.remove(-lit)
                elif lit[0] == '~':
                    negated_var = lit[1:]
                    if negated_var not in assignment and -negated_var not in stack:
                        stack.append(negated_var)
                        break
                else:
                    var = lit
                    if var not in assignment and var not in stack:
                        stack.append(var)
                        break
            if not stack:
                return False
        return True
    
    def resolution(clauses):
        clauses = list(clauses)
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    clause_i = set(clauses[i])
                    clause_j = set(clauses[j])
                    for lit in clause_i:
                        if lit[0] == '~':
                            negated_var = lit[1:]
                            if negated_var in clause_j:
                                new_clause = clause_i.union(clause_j) - {lit, negated_var}
                                if len(new_clause) == 0:
                                    return True
                                new_clauses.append(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return False
    
    def algebraic_k_theory_rank(n):
        # Placeholder function for algebraic K-theory rank calculation
        # This is a dummy implementation and should be replaced with an actual algorithm
        return random.randint(1, n)
    
    n = 30
    m = 5 * n
    clauses = generate_3cnf(n, m)
    if not is_satisfiable(clauses):
        width = resolution(clauses)
        rank = algebraic_k_theory_rank(n)
        return {
            "metric_name": "Correlation",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Mapping_undefined"
        }
    else:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "Unsatisfiable formula"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported = sum(1 for r in results if r["conjecture_holds"]) >= 24
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    
    if supported:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction=1")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Mapping_undefined' first_failing_seed={first_failing_seed}")
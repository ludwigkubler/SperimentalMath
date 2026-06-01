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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
            for j in range(i+1, n+1):
                clauses.append([variables[i-1], f'~{variables[j-1]}'])
        return variables, clauses
    
    def min_diophantine_root_count(clauses):
        algebraic_numbers = set()
        for clause in clauses:
            for literal in clause:
                if literal.startswith('~'):
                    algebraic_numbers.add(literal[1:])
                else:
                    algebraic_numbers.add(literal)
        return len(algebraic_numbers)
    
    def dpll_solver(variables, clauses):
        n = len(variables)
        assignment = [None] * n
        stack = []
        
        def backtrack():
            if all(assignment):
                return True
            i = next(i for i in range(n) if assignment[i] is None)
            assignment[i] = True
            if dpll_helper(clauses, assignment):
                return True
            assignment[i] = False
            if dpll_helper(clauses, assignment):
                return True
            assignment[i] = None
            return False
        
        def dpll_helper(clauses, assignment):
            while stack:
                literal = stack.pop()
                i = variables.index(literal)
                assignment[i] = not assignment[i]
                if backtrack():
                    return True
                assignment[i] = not assignment[i]
            for clause in clauses:
                unsatisfied = any(assignment[variables.index(lit)] is None or 
                                   (lit.startswith('~') and assignment[variables.index(lit[1:])]) 
                                   for lit in clause)
                if unsatisfied:
                    stack.append(next(lit for lit in clause if assignment[variables.index(lit)] is None))
            return False
        
        backtrack()
        return len([v for v in assignment if v is not None])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_length = 0
    total_count = 0
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        count = min_diophantine_root_count(clauses)
        length = dpll_solver(variables, clauses)
        results.append((n, count, length))
        total_length += length
        total_count += count
    
    mean_length = Fraction(total_length) / len(results)
    mean_count = Fraction(total_count) / len(results)
    
    correlation_coefficient = sum((x - mean_count) * (y - mean_length) for n, x, y in results) / len(results)
    max_n = max(n for n, _, _ in results)
    
    if correlation_coefficient < 0.8:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": float(correlation_coefficient),
            "instances_tested": len(results),
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": f"Correlation coefficient {correlation_coefficient} < 0.8"
        }
    
    if any(count > 2 * length for _, count, length in results):
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": float(correlation_coefficient),
            "instances_tested": len(results),
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": f"MinRootCount > 2 * ProofLength for some instances"
        }
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8 or MinRootCount > 2 * ProofLength\" first_failing_seed={first_failing_seed}")
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

def generate_tseitin_formula(w):
    variables = list(range(1, 2 * w + 1))
    clauses = []
    
    for i in range(w):
        clause = [-variables[2 * w + i], -variables[2 * w + (i + 1) % w], variables[i]]
        clauses.append(clause)
        clause = [variables[2 * w + i], variables[2 * w + (i + 1) % w], -variables[i]]
        clauses.append(clause)
    
    for j in range(w):
        for k in range(j + 1, w):
            clause = [-variables[j], -variables[k], variables[2 * w + j + k]]
            clauses.append(clause)
            clause = [variables[j], variables[k], -variables[2 * w + j + k]]
            clauses.append(clause)
    
    return clauses

def is_satisfiable(clauses):
    stack = []
    assignment = {}
    
    for literal in range(1, 2 * len(clauses) + 1):
        if literal not in assignment and -literal not in assignment:
            stack.append(literal)
            assignment[literal] = True
    
    while stack:
        literal = stack.pop()
        if literal < 0:
            literal = -literal
            assignment[literal] = False
        
        found_unsat_clause = False
        for clause in clauses:
            if literal in clause and not any(-l in assignment and not assignment[-l] for l in clause):
                found_unsat_clause = True
                break
        
        if found_unsat_clause:
            for l in clause:
                if -l not in stack:
                    stack.append(-l)
    
    return all(assignment[lit] == (lit > 0) for lit in assignment)

def compute_minimal_index(clauses):
    n = len(clauses)
    variables = set(abs(lit) for clause in clauses for lit in clause)
    variable_count = len(variables)
    
    if variable_count == 0:
        return 1
    
    min_index = float('inf')
    
    for i in range(2 ** variable_count):
        assignment = {variables[j]: (i >> j) & 1 for j in range(variable_count)}
        if all(lit > 0 and assignment[abs(lit)] == (lit > 0) or lit < 0 and not assignment[-lit] for clause in clauses for lit in clause):
            min_index = min(min_index, sum(assignment[var] != assignment[-var] for var in variables))
    
    return min_index

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    w = n // 2
    
    clauses = generate_tseitin_formula(w)
    if not is_satisfiable(clauses):
        return {
            "metric_name": "minimal_index",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }
    
    min_index = compute_minimal_index(clauses)
    
    if min_index < 2 ** (w / 10):
        return {
            "metric_name": "minimal_index",
            "metric_value": min_index,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"min_index={min_index} < 2^(w/10)={2 ** (w / 10)}"
        }
    
    return {
        "metric_name": "minimal_index",
        "metric_value": min_index,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break
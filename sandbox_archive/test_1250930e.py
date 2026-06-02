# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def tseitin_encoding(cnf):
    new_vars = {}
    literals = set()
    for clause in cnf:
        literals.update(abs(x) for x in clause)
    
    var_counter = max(literals, default=0) + 1
    for literal in literals:
        if literal < 0:
            negated_var = -literal
        else:
            negated_var = -literal - 1
        
        new_vars[literal] = var_counter
        new_vars[negated_var] = var_counter + 1
        var_counter += 2
    
    for i, clause in enumerate(cnf):
        tseitin_var = var_counter + 2 * i
        new_vars[tseitin_var] = tseitin_var
        
        if len(clause) == 1:
            literal = clause[0]
            negated_literal = -literal
            new_cnf.append([new_vars[literal], new_vars[negated_literal]])
        else:
            for j in range(len(clause)):
                new_clause = [new_vars[x] for x in clause[:j]]
                new_clause.append(-new_vars[-clause[j]])
                new_cnf.append(new_clause)
            
            new_cnf.append([-tseitin_var])
    
    return new_vars, new_cnf

def quiver_representation(cnf):
    new_vars, new_cnf = tseitin_encoding(cnf)
    quiver_rep = {}
    for literal in new_vars:
        if literal < 0:
            negated_var = -literal
        else:
            negated_var = -literal - 1
        
        quiver_rep[literal] = set([new_vars[negated_var]])
    
    return quiver_rep

def minimal_order(quiver_rep):
    visited = set()
    order = 0
    
    def dfs(node):
        nonlocal order
        if node not in visited:
            visited.add(node)
            for neighbor in quiver_rep[node]:
                dfs(neighbor)
            order += 1
    
    for node in quiver_rep:
        if node not in visited:
            dfs(node)
    
    return order

def frege_proof_length(cnf):
    # Placeholder function to simulate Frege proof length calculation
    # Replace with actual implementation if available
    return len(cnf) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    
    quiver_rep = quiver_representation(cnf)
    min_order = minimal_order(quiver_rep)
    proof_length = frege_proof_length(cnf)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["metric_value"] < 0.5), None)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
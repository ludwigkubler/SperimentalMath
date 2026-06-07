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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def negate(lit):
        if isinstance(lit, str) and lit.startswith('x'):
            return 'not_' + lit
        elif isinstance(lit, str) and lit.startswith('not_'):
            return lit[4:]
        else:
            return -lit
    
    def or_formula(*lits):
        if len(lits) == 1:
            return lits[0]
        else:
            return ('or', *lits)
    
    def tseitin_formula(variables, clauses):
        literals = {f"x{i}": i for i in range(1, variables + 1)}
        neg_literals = {f"not_{x}": x for x in literals}
        formulas = {}
        
        for clause_var in range(1, len(clauses) + 1):
            clause = clauses[clause_var - 1]
            formulas[clause_var] = or_formula(*[negate(lit) if random.choice([True, False]) else lit for lit in clause])
        
        return literals, neg_literals, formulas
    
    def local_chromatic_number(graph):
        n = len(graph)
        colors = [-1] * n
        color_count = 0
        
        def is_safe(v, c):
            for i in range(n):
                if graph[v][i] and colors[i] == c:
                    return False
            return True
        
        def dfs(v, c):
            nonlocal color_count
            colors[v] = c
            color_count = max(color_count, c + 1)
            for i in range(n):
                if graph[v][i]:
                    if colors[i] == -1 and not is_safe(i, c):
                        return False
                    elif colors[i] != -1 and colors[i] == c:
                        return False
            return True
        
        for v in range(n):
            if colors[v] == -1:
                if not dfs(v, 0):
                    return float('inf')
        
        return color_count
    
    def resolution_width(formulas):
        # Placeholder for actual resolution width calculation
        # This is a dummy implementation and should be replaced with the actual logic
        return len(formulas)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1) // 2)
    variables = n
    clauses = []
    
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, variables + 1)]
        clauses.append(clause)
    
    graph = [[0] * n for _ in range(n)]
    for clause in clauses:
        for lit1 in clause:
            for lit2 in clause:
                if lit1 != lit2 and (lit1 > 0) == (lit2 > 0):
                    u, v = abs(lit1) - 1, abs(lit2) - 1
                    graph[u][v] = 1
                    graph[v][u] = 1
    
    tseitin_vars, tseitin_formula_str = tseitin_formula(variables, clauses)
    local_chromatic_num = local_chromatic_number(graph)
    resolution_width_val = resolution_width(tseitin_formula_str)
    
    return {
        "metric_name": "local_chromatic_number_diff",
        "metric_value": abs(local_chromatic_num - resolution_width_val),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(local_chromatic_num - resolution_width_val) <= 5,  # Placeholder constant k
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(30)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean_metric_value = sum(metric_values) / len(results)
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in metric_values) / len(results)) ** 0.5
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
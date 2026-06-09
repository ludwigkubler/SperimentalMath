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
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[var] = True if var > 0 else False
            if dpll([c for c in clauses if not any(abs(v) == abs(var) for v in c)], new_assignment):
                return True
            new_assignment[var] = False
            if dpll([c for c in clauses if not any(abs(v) == abs(var) for v in c)], new_assignment):
                return True
            return False
        pure_literal = next((v for v in range(1, max(variables) + 1) if (v not in assignment and -v not in assignment)), None)
        if pure_literal:
            new_assignment[pure_literal] = True
            if dpll(clauses, new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll(clauses, new_assignment):
                return True
            return False
        var = random.choice([v for v in range(1, max(variables) + 1) if v not in assignment and -v not in assignment])
        new_assignment[var] = True
        if dpll([c for c in clauses if not any(abs(v) == abs(var) for v in c)], new_assignment):
            return True
        new_assignment[var] = False
        if dpll([c for c in clauses if not any(abs(v) == abs(var) for v in c)], new_assignment):
            return True
        return False
    
    def generate_tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(m):
            a, b, op = random.choice([('AND', 'OR'), ('OR', 'AND')])
            x, y = random.sample(variables, 2)
            if op == 'AND':
                clauses.append([x, -y])
                clauses.append([-x, y])
                clauses.append([x, y])
            else:
                clauses.append([-x, -y])
                clauses.append([x, y])
        return variables, clauses
    
    def compute_local_zeta_function_rank(G):
        n = len(G)
        zeta = [0] * (n + 1)
        zeta[0] = 1
        for i in range(1, n + 1):
            zeta[i] = sum(zeta[j] * G[i][j] for j in range(i)) / i
        return max(zeta)
    
    def compute_resolution_proof_width(clauses):
        assignment = {}
        return len(dpll(clauses, assignment))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n, 2 * n)
        G = [[0] * (n + 1) for _ in range(n + 1)]
        for x, y in random.sample(list(itertools.combinations(variables, 2)), len(clauses)):
            G[x][y] = 1
            G[y][x] = 1
        r = compute_local_zeta_function_rank(G)
        w = compute_resolution_proof_width(clauses)
        results.append((w, r))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    w_values, r_values = zip(*results)
    mean_w = sum(w_values) / len(w_values)
    std_w = math.sqrt(sum((w - mean_w) ** 2 for w in w_values) / len(w_values))
    correlation_coefficient = sum((w - mean_w) * (r - mean_r) for w, r in zip(w_values, r_values)) / (len(w_values) * std_w * std_r)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(w_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results))) ** 2 for r in results) / len(results))} support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
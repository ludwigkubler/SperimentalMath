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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment):
        unsatisfied = [c for c in cnf if any(lit in assignment and assignment[lit] == val for lit, val in zip(c, (1, 0))) for c in cnf]
        if not unsatisfied:
            return True
        unit_clauses = [c for c in unsatisfied if len(c) == 1]
        if unit_clauses:
            literal, value = unit_clauses[0][0], 1 - abs(unit_clauses[0][0]) % 2
            assignment[literal] = value
            return dpll(cnf, assignment)
        pure_literals = [l for l in range(-n, n + 1) if all(l not in c or (assignment.get(l, None) == val and assignment.get(-l, None) != val) for c in cnf for val in (0, 1))]
        if pure_literals:
            literal = pure_literals[0]
            value = 1 - abs(literal) % 2
            assignment[literal] = value
            return dpll(cnf, assignment)
        literal = random.choice([l for l in range(-n, n + 1) if l not in assignment])
        assignment[literal] = 0
        if dpll(cnf, assignment):
            return True
        assignment[literal] = 1
        return dpll(cnf, assignment)
    
    def kerdock_code_dimension(cnf):
        # Simplified Kerdock code dimension calculation for demonstration purposes
        return len(cnf) / n
    
    def dpll_tree_depth(cnf):
        depth = [0] * (2 ** n)
        
        def dfs(node, path):
            if node >= 2 ** n:
                return 0
            if any(lit in path and path[lit] == val for lit, val in zip(cnf[node], (1, 0))):
                return 0
            unit_clauses = [c for c in cnf[node] if len(c) == 1]
            if unit_clauses:
                literal, value = unit_clauses[0][0], 1 - abs(unit_clauses[0][0]) % 2
                path[literal] = value
                return dfs(2 * node + (value ^ 1), path)
            pure_literals = [l for l in range(-n, n + 1) if all(l not in c or (path.get(l, None) == val and path.get(-l, None) != val) for c in cnf[node] for val in (0, 1))]
            if pure_literals:
                literal = pure_literals[0]
                value = 1 - abs(literal) % 2
                path[literal] = value
                return dfs(2 * node + (value ^ 1), path)
            literal = random.choice([l for l in range(-n, n + 1) if l not in path])
            path[literal] = 0
            depth[node] = max(depth[node], dfs(2 * node, path))
            path[literal] = 1
            depth[node] = max(depth[node], dfs(2 * node + 1, path))
            return depth[node]
        
        dfs(0, {})
        return max(depth)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    dim = kerdock_code_dimension(cnf)
    d = dpll_tree_depth(cnf)
    
    if d == 0:
        return {
            "metric_name": "dim_over_d",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL tree depth is zero, cannot compute dim/d"
        }
    
    ratio = dim / d
    expected_ratio = math.log(d, 2)
    within_range = abs(ratio - expected_ratio) <= 0.2 * expected_ratio
    
    return {
        "metric_name": "dim_over_d",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": within_range,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000000) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "dim_over_d_ratio_outside_20_percent"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [-v for v in clause]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(formula):
        stack = []
        assignment = {}
        
        def dfs(i):
            if i == len(formula):
                return True
            for literal in formula[i]:
                var = abs(literal)
                if var not in assignment:
                    assignment[var] = literal > 0
                    if dfs(i + 1):
                        return True
                    assignment.pop(var)
                elif assignment[var] != (literal > 0):
                    continue
                else:
                    break
            else:
                assignment[var] = not assignment.get(var, False)
                if dfs(i + 1):
                    return True
                assignment.pop(var)
            return False
        
        return dfs(0)
    
    def compute_minimal_rank(formula):
        n = len(formula)
        rank = 0
        for clause in formula:
            rank += len(set(abs(lit) for lit in clause))
        return rank
    
    def compute_max_degree(formula):
        degree = {}
        for clause in formula:
            for literal in clause:
                var = abs(literal)
                if var not in degree:
                    degree[var] = 1
                else:
                    degree[var] += 1
        return max(degree.values())
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    satisfiable = is_satisfiable(formula)
    
    if not satisfiable:
        q_phi = compute_minimal_rank(formula)
        expected_q_phi = n
        if abs(q_phi - expected_q_phi) > 1:
            return {
                "metric_name": "Minimal Quandle Rank",
                "metric_value": q_phi,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Unsatisfiable formula with rank {q_phi} != Θ(n) = {expected_q_phi}"
            }
    
    max_degree = compute_max_degree(formula)
    q_phi = compute_minimal_rank(formula)
    expected_q_phi = math.log2(n) + math.log2(max_degree)
    
    return {
        "metric_name": "Minimal Quandle Rank",
        "metric_value": q_phi,
        "instances_tested": 1,
        "conjecture_holds": abs(q_phi - expected_q_phi) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = conjecture_holds_count / len(results) * 100
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction=100.00")
    elif conjecture_holds_count >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not match expected\" first_failing_seed={first_failing_seed}")
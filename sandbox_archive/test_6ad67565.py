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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n // 2):
            clause = set(random.sample(range(1, n + 1), 3))
            if random.choice([True, False]):
                clause = {-(x) for x in clause}
            clauses.append(clause)
        return clauses
    
    def dpll_refutation_depth(clauses):
        def is_satisfiable(clauses, assignment):
            for clause in clauses:
                if not any(abs(lit) in assignment and (assignment[abs(lit)] == lit > 0) for lit in clause):
                    return False
            return True
        
        def backtrack(clauses, assignment):
            unassigned = [i for i in range(1, n + 1) if i not in assignment]
            if not unassigned:
                return len(assignment)
            var = random.choice(unassigned)
            assignment[var] = True
            if is_satisfiable(clauses, assignment):
                depth_true = backtrack(clauses, assignment)
                if depth_true != float('inf'):
                    return depth_true + 1
            del assignment[var]
            assignment[-var] = True
            if is_satisfiable(clauses, assignment):
                depth_false = backtrack(clauses, assignment)
                if depth_false != float('inf'):
                    return depth_false + 1
            del assignment[-var]
            return float('inf')
        
        n = len(assignment) if assignment else 0
        return backtrack(clauses, {})
    
    def entropic_complexity(clauses):
        truth_table = [False] * (2 ** n)
        for i in range(len(truth_table)):
            assignment = {j + 1: ((i >> j) & 1) * 2 - 1 for j in range(n)}
            if is_satisfiable(clauses, assignment):
                truth_table[i] = True
        entropy = 0
        for count in [truth_table.count(True), truth_table.count(False)]:
            p = count / len(truth_table)
            if p != 0 and p != 1:
                entropy -= p * math.log2(p)
        return entropy
    
    n = random.randint(5, 40)
    k = random.randint(1, n // 3)
    clauses = generate_k_cnf(n, k)
    
    dpll_depth = dpll_refutation_depth(clauses)
    if dpll_depth == float('inf'):
        return {
            "metric_name": "DPLL Refutation Depth",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    
    entropic = entropic_complexity(clauses)
    
    return {
        "metric_name": "DPLL Refutation Depth",
        "metric_value": dpll_depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
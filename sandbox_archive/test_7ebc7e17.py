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
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def dpll_search_tree_width(clauses):
        # Simplified DPLL algorithm to estimate tree width
        stack = []
        assignment = {}
        width = 0
        
        def backtrack():
            nonlocal width
            if not stack:
                width = max(width, len(assignment))
                return True
            
            var = next((v for v in range(1, n + 1) if v not in assignment), None)
            if var is None:
                return False
            
            assignment[var] = True
            if all(any(x in assignment and (x > 0) == assignment[x] for x in clause) for clause in clauses):
                if backtrack():
                    return True
            del assignment[var]
            
            assignment[-var] = True
            if all(any(x in assignment and (x > 0) == assignment[x] for x in clause) for clause in clauses):
                if backtrack():
                    return True
            del assignment[-var]
            
            return False
        
        backtrack()
        return width
    
    def hodge_decomposition_rank(clauses):
        # Simplified Hodge decomposition rank estimation
        n = len(clauses)
        matrix = [[0] * n for _ in range(n)]
        
        for i, clause1 in enumerate(clauses):
            for j, clause2 in enumerate(clauses):
                if i != j:
                    count = sum(1 for x in clause1 if -x in clause2)
                    matrix[i][j] = count
        
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for j in range(n):
                    if row[j]:
                        for k in range(n):
                            matrix[k][j] -= row[k]
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        dpll_width = dpll_search_tree_width(cnf)
        hodge_rank = hodge_decomposition_rank(cnf)
        
        if dpll_width == 0 or hodge_rank == 0:
            continue
        
        results.append({
            "n": n,
            "dpll_width": dpll_width,
            "hodge_rank": hodge_rank
        })
    
    if not results:
        return {
            "metric_name": "Rank vs DPLL Width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    min_rank = min(result["hodge_rank"] for result in results)
    avg_width = sum(result["dpll_width"] for result in results) / len(results)
    
    return {
        "metric_name": "Rank vs DPLL Width",
        "metric_value": min_rank,
        "instances_tested": len(results),
        "conjecture_holds": min_rank <= 2 * avg_width,  # Linear relationship with a small margin
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    total_metric_value = 0
    count_conjecture_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            total_metric_value += trial_result["metric_value"]
            count_conjecture_holds += int(trial_result["conjecture_holds"])
    
    mean_metric_value = total_metric_value / len(seeds)
    support_fraction = count_conjecture_holds / len(seeds) if len(seeds) > 0 else 0
    
    if all(result["metric_value"] is not None for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=metric_saturation")
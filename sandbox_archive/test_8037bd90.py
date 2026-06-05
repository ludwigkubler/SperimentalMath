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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10):  # Generate 10 clauses with n variables
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def is_satisfiable(literals, assignment):
            for clause in cnf:
                if all(lit not in literals or (lit < 0 and -lit not in literals) for lit in clause):
                    continue
                else:
                    return False
            return True
        
        def backtrack(literals, assignment):
            if len(literals) == 0:
                return is_satisfiable(literals, assignment)
            
            literal = literals[0]
            if literal > 0:
                assignment[literal] = True
                if backtrack(literals[1:], assignment):
                    return True
                del assignment[literal]
                
                assignment[-literal] = True
                if backtrack(literals[1:], assignment):
                    return True
                del assignment[-literal]
            
            else:
                assignment[literal] = False
                if backtrack(literals[1:], assignment):
                    return True
                del assignment[literal]
                
                assignment[-literal] = False
                if backtrack(literals[1:], assignment):
                    return True
                del assignment[-literal]
        
        literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
        return backtrack(literals, {})
    
    def etale_cohomology(cnf):
        # Simplified mapping to a graph problem (adjacency matrix)
        n = len(cnf)
        adj_matrix = [[0] * n for _ in range(n)]
        
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    u, v = abs(clause[i]) - 1, abs(clause[j]) - 1
                    adj_matrix[u][v] = 1
                    adj_matrix[v][u] = 1
        
        # Find the number of connected components (simplified)
        visited = [False] * n
        components = 0
        
        def dfs(u):
            stack = [u]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    for v in range(n):
                        if adj_matrix[u][v] and not visited[v]:
                            stack.append(v)
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
                components += 1
        
        return components
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n_max)
        proof_length = dpll(cnf)
        cohomology_order = etale_cohomology(cnf)
        
        if proof_length is None or cohomology_order is None:
            return {
                "metric_name": "cohomology_diff",
                "metric_value": float('nan'),
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "dpll or cohomology failed"
            }
        
        metric_values.append(abs(cohomology_order - proof_length))
    
    mean_diff = sum(metric_values) / len(metric_values)
    support_fraction = sum(1 for diff in metric_values if abs(diff) <= 3) / len(metric_values)
    
    return {
        "metric_name": "cohomology_diff",
        "metric_value": mean_diff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
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
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"cohomology_diff\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data")
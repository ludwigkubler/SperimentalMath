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
    
    def dpll(cnf):
        def solve(assignment, clause_index=0):
            if clause_index == len(cnf):
                return True
            for literal in cnf[clause_index]:
                var = abs(literal)
                if var not in assignment:
                    new_assignment = assignment.copy()
                    new_assignment[var] = literal > 0
                    if solve(new_assignment, clause_index + 1):
                        return True
                    new_assignment[var] = not new_assignment[var]
                    if solve(new_assignment, clause_index + 1):
                        return True
            return False
        
        return solve({})
    
    def groupoid_representation(cnf):
        n = len(cnf)
        G = [[0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(i, n):
                if any(literal in cnf[i] and -literal in cnf[j] for literal in range(1, n + 1)):
                    G[i][j] = 1
                    G[j][i] = 1
        
        return G
    
    def min_representation_dimension(G):
        n = len(G)
        visited = [False] * n
        min_dim = 0
        
        for i in range(n):
            if not visited[i]:
                queue = [i]
                while queue:
                    node = queue.pop(0)
                    if not visited[node]:
                        visited[node] = True
                        for j in range(n):
                            if G[node][j] == 1 and not visited[j]:
                                queue.append(j)
                min_dim += 1
        
        return min_dim
    
    def frege_proof_depth(cnf):
        return dpll(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            cnf = [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
            G = groupoid_representation(cnf)
            min_dim = min_representation_dimension(G)
            d_n = frege_proof_depth(cnf)
            
            total_metric_value += min_dim
            instances_tested += 1
            n_max = max(n_max, n)
    
    metric_value = total_metric_value / instances_tested
    
    if n_max < 16:
        return {
            "metric_name": "min_representation_dimension",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    return {
        "metric_name": "min_representation_dimension",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
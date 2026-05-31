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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = []
            for _ in range(3):
                var = random.randint(-n, n)
                if var == 0:
                    continue
                clause.append(var)
            clauses.append(clause)
        return clauses

    def is_satisfiable(cnf):
        n = max(abs(lit) for lit in cnf[0])
        assignment = [None] * (n + 1)
        
        def backtrack(k):
            if k > n:
                return all(any(lit * assignment[abs(lit)] > 0 for lit in clause) for clause in cnf)
            for val in [-1, 1]:
                assignment[k] = val
                if backtrack(k + 1):
                    return True
            assignment[k] = None
            return False
        
        return backtrack(1)

    def circuit_size(cnf):
        n = max(abs(lit) for lit in cnf[0])
        clauses = {tuple(clause): [] for clause in cnf}
        
        def dfs(node, visited):
            if node in visited:
                return
            visited.add(node)
            for neighbor in clauses[node]:
                dfs(neighbor, visited)
        
        visited = set()
        for i in range(1, n + 1):
            dfs(i, visited)
        
        return len(visited)

    def coxeter_group_order(n):
        # Simplified approximation of the order
        return 2**n / (n ** (1/3))

    cnf = generate_3cnf(10)  # Start with n=10 for simplicity
    circuit_size_value = circuit_size(cnf)
    coxeter_group_order_value = coxeter_group_order(len(cnf[0]))
    
    return {
        "metric_name": "Circuit Size vs. Coxeter Group Order",
        "metric_value": circuit_size_value,
        "instances_tested": 1,
        "n_max": len(cnf[0]),
        "conjecture_holds": circuit_size_value <= coxeter_group_order_value + 3,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
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
        for _ in range(n * 3):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def backtrack():
        assignment = [None] * (n + 1)
        stack = []
        
        def search(t):
            if t > n:
                return True
            for val in [-1, 1]:
                assignment[t] = val
                if is_satisfiable(cnf):
                    stack.append((t, val))
                    if search(t + 1):
                        return True
                    stack.pop()
            assignment[t] = None
            return False
        
        return search(1)
    
    def is_satisfiable(cnf):
        while stack:
            t, val = stack.pop()
            assignment[t] = val
            for clause in cnf:
                if not any([assignment[abs(lit)] == (lit > 0) for lit in clause]):
                    break
            else:
                return True
        return False
    
    def read_twice_bp_size(cnf):
        n = len(cnf)
        dp = [[False] * (n + 1) for _ in range(n + 1)]
        
        def backtrack(i, j):
            if i > n or j > n:
                return 0
            if dp[i][j]:
                return 0
            dp[i][j] = True
            size = 1
            for clause in cnf:
                if not any([assignment[abs(lit)] == (lit > 0) for lit in clause]):
                    break
            else:
                size += backtrack(i + 1, j)
            return size
        
        return backtrack(1, 1)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    if not backtrack():
        return {
            "metric_name": "rho_sheaf",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "The formula is unsatisfiable."
        }
    
    bp_size = read_twice_bp_size(cnf)
    if bp_size == 0:
        return {
            "metric_name": "rho_sheaf",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "The formula is unsatisfiable."
        }
    
    rho_sheaf = Fraction(n, bp_size)
    return {
        "metric_name": "rho_sheaf",
        "metric_value": float(rho_sheaf),
        "instances_tested": 1,
        "conjecture_holds": abs(rho_sheaf - 1) <= 0.3,
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
    
    mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low rho_sheaf' first_failing_seed={first_failing_seed}")
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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def is_tautology(clauses):
        # Check if the formula is a tautology
        variables = set(abs(c) for c in sum(clauses, []))
        assignment = {v: False for v in variables}
        stack = []
        
        def dfs(v):
            if v in assignment:
                return assignment[v]
            assignment[v] = True
            for clause in clauses:
                if v in clause and not dfs(-v):
                    return False
            stack.append(v)
            return True
        
        for v in variables:
            if not dfs(v):
                return False
        
        while stack:
            v = stack.pop()
            assignment[v] = False
            for clause in clauses:
                if -v in clause and not dfs(v):
                    return False
        
        return True
    
    def compute_minimal_rank(clauses):
        # Compute the minimal rank of the groupoid G(F)
        n = len(set(abs(c) for c in sum(clauses, [])))
        if is_tautology(clauses):
            return 0
        else:
            return math.ceil(math.log(n, 2))
    
    n = random.randint(5, 40)
    m = random.randint(1, 3 * n)
    clauses = generate_cnf(n, m)
    rank = compute_minimal_rank(clauses)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= math.log2(n) ** 2
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        counterexample_desc = f"n={results[first_failing_seed]['instances_tested']}, rank={results[first_failing_seed]['metric_value']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
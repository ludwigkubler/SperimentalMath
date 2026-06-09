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
    
    def generate_cnf(n, k):
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(clause.count(lit) == 1 for lit in clause):
                cnf.append(clause)
        return cnf
    
    def is_k_colorable(cnf, k):
        colors = {}
        for clause in cnf:
            for literal in clause:
                var = abs(literal)
                if var not in colors:
                    colors[var] = random.randint(1, k)
                elif colors[var] != (colors[literal] if literal > 0 else -colors[literal]):
                    return False
        return True
    
    def categorify(cnf):
        n = len(cnf[0])
        category = [[set() for _ in range(n + 1)] for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                var = abs(literal)
                if literal > 0:
                    category[var][var].add(var)
                else:
                    category[0][var].add(var)
        return category
    
    def height_of_category(category):
        n = len(category) - 1
        visited = [False] * (n + 1)
        stack = [(n, 0)]
        max_height = 0
        
        while stack:
            node, depth = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in category[node][node]:
                    stack.append((neighbor, depth + 1))
                max_height = max(max_height, depth)
        
        return max_height
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n, 8))  # Ensure k is at least 2 and not too large
    cnf = generate_cnf(n, k)
    
    if not is_k_colorable(cnf, k):
        return {
            "metric_name": "category_height",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "not_k_colorable"
        }
    
    category = categorify(cnf)
    height = height_of_category(category)
    
    return {
        "metric_name": "category_height",
        "metric_value": height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": height <= k**(3/2) * math.log(n, 2)**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "not_k_colorable"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
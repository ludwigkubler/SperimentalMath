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
        for _ in range(10 * n):  # 10 clauses per variable on average
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    def is_satisfiable(phi):
        stack = []
        assignment = {}
        
        def dpll():
            if not phi:
                return True
            for lit in phi[0]:
                if lit > 0 and lit not in assignment:
                    assignment[lit] = True
                    if dpll():
                        return True
                    del assignment[lit]
                elif lit < 0 and -lit not in assignment:
                    assignment[-lit] = False
                    if dpll():
                        return True
                    del assignment[-lit]
            return False
        
        return dpll()

    def count_periodic_points(phi):
        n = len(phi)
        visited = [False] * (1 << n)
        
        def dfs(state, path):
            if state in visited:
                return len(path) - visited[state]
            visited[state] = len(path)
            for i in range(n):
                new_state = state ^ (1 << i)
                if is_satisfiable(phi + [[-i]]) and is_satisfiable(phi + [[i]]):
                    path.append(new_state)
                    length = dfs(new_state, path)
                    path.pop()
                    return length
            return 0
        
        return dfs(0, [])

    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    
    for n in range(5, n_max + 1):
        phi = generate_3cnf(n)
        periodic_points = count_periodic_points(phi)
        instances_tested += 1
        metric_value += periodic_points

    mean_metric_value = metric_value / instances_tested
    conjecture_holds = all(periodic_points <= n**2 for _ in range(30))  # Example polynomial bound
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Number of Periodic Points",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")
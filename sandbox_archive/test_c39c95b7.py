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
    
    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for literal in literals:
            clauses.append([literal])
        for i in range(1, n):
            clauses.append([f'-x{i}', f'x{i+1}'])
        clauses.append([f'-x{n}'])
        return literals, clauses
    
    def resolution(clauses):
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i = set(clauses[i])
                    clause_j = set(clauses[j])
                    if not (clause_i & clause_j):
                        continue
                    new_clause = clause_i ^ clause_j
                    if len(new_clause) == 0:
                        return False
                    new_clauses.append(list(new_clause))
            if new_clauses == clauses:
                break
            clauses = new_clauses
        return True
    
    def geometric_flow(clauses):
        n = len(clauses)
        flow_time = 0
        while True:
            for i in range(n):
                for j in range(i + 1, n):
                    if resolution([clauses[i], clauses[j]]):
                        flow_time += 1
                        break
                else:
                    continue
                break
            else:
                return flow_time
    
    def resolution_width(clauses):
        visited = set()
        queue = [([], clauses)]
        while queue:
            path, remaining_clauses = queue.pop(0)
            if not remaining_clauses:
                return len(path)
            literal = remaining_clauses[0][0]
            for clause in remaining_clauses:
                if literal in clause:
                    new_path = path + [literal]
                    new_remaining_clauses = [c for c in remaining_clauses if literal not in c]
                    queue.append((new_path, new_remaining_clauses))
        return float('inf')
    
    n = random.randint(5, 40)
    literals, clauses = tseitin_formula(n)
    flow_time = geometric_flow(clauses)
    width = resolution_width(clauses)
    
    if width == float('inf'):
        return {
            "metric_name": "flow_to_width_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    ratio = flow_time / width
    return {
        "metric_name": "flow_to_width_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results):.2f} std=NOT_APPLICABLE support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"flow_to_width_ratio_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
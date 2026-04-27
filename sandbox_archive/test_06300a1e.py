# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def lex_dpll(cnf, assignment):
    def dfs():
        if not cnf:
            return True
        var = next((v for v in range(len(cnf)) if v not in assignment), None)
        if var is None:
            return False
        
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            new_cnf = []
            for clause in cnf:
                if any(var == v and val == True or var == -v and val == False for v in clause):
                    continue
                elif all(var == -v or var == v for v in clause):
                    return False
                else:
                    new_clause = [v for v in clause if v != var and v != -var]
                    if new_clause:
                        new_cnf.append(new_clause)
            if dfs():
                return True
        return False
    
    return dfs()

def herbrand_disjunction_length(cnf):
    n = len(cnf)
    variables = set()
    for clause in cnf:
        variables.update(abs(v) for v in clause)
    
    def covers(assignment):
        for clause in cnf:
            if all(var not in assignment or (var < 0 and assignment[var] == False) or (var > 0 and assignment[var] == True) for var in clause):
                return False
        return True
    
    min_cover = float('inf')
    for i in range(1 << len(variables)):
        assignment = {v: bool(i & (1 << j)) for j, v in enumerate(variables)}
        if covers(assignment):
            min_cover = min(min_cover, sum(1 for var, val in assignment.items() if val))
    
    return min_cover

def build_php(n):
    variables = set()
    clauses = []
    for i in range(n):
        for j in range(n + 1):
            variables.add(i * (n + 1) + j)
            variables.add(-(i * (n + 1) + j))
    
    for i in range(n):
        for j in range(n + 1):
            clauses.append([-(i * (n + 1) + j)])
    
    for i in range(n):
        for j in range(n + 1):
            for k in range(j + 1, n + 1):
                clauses.append([(i * (n + 1) + j), -(i * (n + 1) + k)])
    
    return list(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(3, 11):
        cnf = build_php(n)
        leaves = lex_dpll(cnf, {})
        H = herbrand_disjunction_length(cnf)
        ratio = math.log2(leaves) / math.log2(H)
        results.append((n, leaves, H, ratio))
    
    median_ratio = sorted(ratio for _, _, _, ratio in results)[len(results) // 2]
    conjecture_holds = 0.75 <= median_ratio <= 1.25
    counterexample = "" if conjecture_holds else f"n={results[0][0]}, L_T={results[0][1]}, H={results[0][2]}, ratio={median_ratio}"
    
    return {
        "metric_name": "ratio",
        "metric_value": median_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    ratios = [result["metric_value"] for result in results if "metric_value" in result]
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(0.75 <= r <= 1.25 for r in ratios):
        print(f"RESULT: SUPPORTED mean={sum(ratios)/len(ratios)} std={math.sqrt(sum((r - sum(ratios)/len(ratios))**2 for r in ratios) / len(ratios))} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0][0]}, L_T={results[0][1]}, H={results[0][2]}, ratio={median_ratio}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
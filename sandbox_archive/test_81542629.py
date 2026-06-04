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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate clauses for each variable
        for var in variables:
            clause = [var]
            neg_clause = [-var]
            clauses.append(clause)
            clauses.append(neg_clause)
        
        # Generate clauses for implications
        for i in range(1, n):
            for j in range(i+1, n+1):
                pos_ij = f'x{i} x{j}'
                neg_ij = [-i, -j]
                clauses.append([pos_ij])
                clauses.append(neg_ij)
        
        return clauses
    
    def resolution(clauses):
        clauses = [set(c) for c in clauses]
        new_clauses = set()
        while True:
            new_clauses.clear()
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(clause1 & clause2) == 1:
                        new_clause = (clause1 | clause2) - {list(clause1 & clause2)[0]}
                        if not new_clause:
                            return None
                        new_clauses.add(frozenset(new_clause))
            if new_clauses.issubset(clauses):
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    def hecke_eigenvalues(clauses):
        n = len(clauses[0])
        vector = [0] * ((n + 1) // 2)
        
        for clause in clauses:
            if len(clause) == 1:
                i = abs(int(clause.pop()))
                if i % 2 == 0:
                    vector[(i-1)//2] = 1
                else:
                    vector[(i+1)//2] = -1
        
        N = sum(abs(x) for x in vector)
        return N
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        clauses = generate_tseitin_formula(n)
        width = resolution(clauses)
        if width is None:
            continue
        N = hecke_eigenvalues(clauses)
        if N == 0:
            continue
        metric_value = width / math.sqrt(N)
        metric_values.append(metric_value)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(m <= 3 for m in metric_values)
    counterexample = "" if conjecture_holds else f"correlation_coefficient={mean_metric_value}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_metric_value,
        "instances_tested": len(metric_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")
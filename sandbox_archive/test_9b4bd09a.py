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
    
    def generate_cnf(n: int, m: int):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        width = 0
        while True:
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted([l for l in clause1 + clause2 if l not in (set(clause1) & set(clause2))]))
                        if new_clause not in clauses and new_clause not in new_clauses:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
            width += 1
        return width
    
    def quantum_logic_rank(cnf):
        n = max(abs(l) for clause in cnf for l in clause)
        rank = 0
        for j in range(2**n):
            if all(l in clause or -l in clause for l in bin(j)[2:].zfill(n)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0
    total_width = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(10, 20))
            rank = quantum_logic_rank(cnf)
            width = resolution_width(cnf)
            instances_tested += 1
            total_rank += rank
            total_width += width
            max_n = max(max_n, n)
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    correlation_coefficient = (instances_tested * sum(rank * width for rank, width in zip(range(instances_tested), range(instances_tested))) - total_rank * total_width) / ((instances_tested * sum(rank**2 for rank in range(instances_tested)) - total_rank**2) ** 0.5 * (instances_tested * sum(width**2 for width in range(instances_tested)) - total_width**2) ** 0.5)
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": max_n,
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
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
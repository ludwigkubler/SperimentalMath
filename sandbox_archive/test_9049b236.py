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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = set(tuple(sorted(c)) for c in cnf)
        width = 1
        
        while True:
            new_clauses = []
            for c1, c2 in itertools.combinations(clauses, 2):
                if any(abs(l) == abs(m) and l != m for l in c1 for m in c2):
                    new_clause = [l for l in c1 + c2 if l not in (abs(l), -abs(l))]
                    new_clauses.append(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.update(new_clauses)
            width += 1
        
        return width
    
    def quantum_logic_rank(cnf):
        n = len(cnf[0])
        matrix = [[0] * (2**n) for _ in range(2**n)]
        
        for i, clause in enumerate(cnf):
            for j in range(2**n):
                if all(l in clause or -l in clause for l in bin(j)[2:].zfill(n)):
                    matrix[i][j] = 1
        
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for i in range(2**n):
                    if row[i]:
                        for j in range(2**n):
                            if matrix[j][i]:
                                matrix[j] = [x - y for x, y in zip(matrix[j], row)]
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_width = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            rank = quantum_logic_rank(cnf)
            width = resolution_width(cnf)
            
            if rank == 0 or width == 0:
                continue
            
            total_rank += rank
            total_width += width
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    correlation_coefficient = (mean_rank * mean_width - instances_tested) / (instances_tested**2 - instances_tested)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and correlation_coefficient < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[support_fraction < 0.8][0]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=metric_saturation_or_tautological_inequality")
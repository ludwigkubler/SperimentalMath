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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(cnf) + 1) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                elif -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        def backtrack(lit):
            assignment.pop()
        
        if dpll(propagate(literal), assignment + [literal]):
            return True
        backtrack(literal)
        
        if dpll(propagate(-literal), assignment + [-literal]):
            return True
        backtrack(-literal)
        
        return False
    
    def frobenius_schur_indicator(matrix):
        n = len(matrix)
        trace = sum(matrix[i][i] for i in range(n))
        det = 1.0
        for row in matrix:
            det *= abs(sum(row[j] * matrix[j][i] for j in range(n)))
        return trace / det
    
    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if set(queue[i]).intersection(set(queue[j])):
                        new_clause = [l for l in queue[i] if l not in queue[j]] + [l for l in queue[j] if -l not in queue[i]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(queue)
            queue.append(new_clause)
    
    n_max = 0
    instances_tested = 0
    total_fsi = 0.0
    total_diff = 0.0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            cnf = generate_cnf(n)
            instances_tested += 1
            
            matrix = [[0] * (n + 1) for _ in range(n + 1)]
            for clause in cnf:
                for l in clause:
                    if l > 0:
                        matrix[l][l] += 1
                    else:
                        matrix[-l][-l] -= 1
            
            fsi = frobenius_schur_indicator(matrix)
            width = resolution_width(cnf)
            
            total_fsi += fsi
            total_diff += abs(fsi - width)
    
    mean_fsi = total_fsi / instances_tested
    mean_diff = total_diff / instances_tested
    
    correlation_coefficient = (instances_tested * sum(fsi * width for fsi, width in zip([mean_fsi] * instances_tested, [mean_diff] * instances_tested)) - instances_tested * mean_fsi * mean_diff) / math.sqrt((instances_tested * sum(fsi**2 for fsi in [mean_fsi] * instances_tested) - instances_tested * mean_fsi**2) * (instances_tested * sum(diff**2 for diff in [mean_diff] * instances_tested) - instances_tested * mean_diff**2))
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_diff <= 3
    
    return {
        "metric_name": "Frobenius-Schur Indicator vs Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Correlation coefficient < 0.8 or mean absolute difference > 3"
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
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8 or mean absolute difference > 3\" first_failing_seed={first_failing_seed}")
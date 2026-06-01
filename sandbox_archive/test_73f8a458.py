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
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        visited = set()
        while queue:
            clause = queue.pop(0)
            if any(l == 0 for l in clause):
                return len(queue) + 1
            for other_clause in queue:
                for lit in clause:
                    if -lit in other_clause:
                        new_lit = [l for l in other_clause if l != -lit]
                        if tuple(new_lit) not in visited:
                            visited.add(tuple(new_lit))
                            queue.append(new_lit)
        return len(queue)
    
    def quantum_logic_rank(cnf):
        n = max(abs(l) for clause in cnf for l in clause)
        identity_matrix = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        A = [identity_matrix]
        
        for clause in cnf:
            row = [Fraction(0, 1)] * n
            for l in clause:
                row[abs(l) - 1] += Fraction(1, 1) if l > 0 else Fraction(-1, 1)
            A.append(row)
        
        while len(A) > 1:
            pivot_row = next(i for i, row in enumerate(A[1:], start=1) if row[0] != Fraction(0, 1))
            A[1], A[pivot_row + 1] = A[pivot_row + 1], A[1]
            
            for i in range(2, len(A)):
                factor = A[i][0] / A[1][0]
                A[i] = [A[i][j] - factor * A[1][j] for j in range(n + 1)]
            
            A.pop(1)
        
        rank = sum(1 for row in A if any(x != Fraction(0, 1) for x in row))
        return rank
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n_max)
        rank = quantum_logic_rank(cnf)
        width = resolution_width(cnf)
        metric_values.append((rank, width))
    
    correlation_coefficient = sum((x[0] - x[1]) * (y[0] - y[1]) for x, y in zip(metric_values, reversed(metric_values))) / len(metric_values) ** 2
    conjecture_holds = correlation_coefficient >= 0.7
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"r = {correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")
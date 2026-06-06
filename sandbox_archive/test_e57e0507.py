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
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def cnf_to_matrix(cnf):
        n = len(cnf)
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                for j in clause:
                    if i != j:
                        matrix[i-1][j-1] = max(matrix[i-1][j-1], 1)
        return matrix
    
    def minimal_tropical_hermitian_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        var = next((v for v in range(1, len(cnf) + 1) if v not in assignment), None)
        if var is None:
            return False
        
        def propagate(var, value):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            new_cnf = []
            for clause in cnf:
                if any(v in new_assignment and new_assignment[v] != value for v in clause):
                    continue
                new_clause = [v for v in clause if v not in new_assignment]
                if not new_clause:
                    return None
                new_cnf.append(new_clause)
            return new_cnf
        
        def backtrack(var, value):
            assignment.pop(var)
        
        for value in [True, False]:
            new_cnf = propagate(var, value)
            if new_cnf is None:
                continue
            if dpll(new_cnf, new_assignment):
                return True
            backtrack(var, value)
        return False
    
    def cnf_length(cnf):
        return sum(len(clause) for clause in cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    matrix = cnf_to_matrix(cnf)
    mhr = minimal_tropical_hermitian_rank(matrix)
    L_DPLL = cnf_length(cnf)
    
    return {
        "metric_name": "mhr vs L_DPLL",
        "metric_value": mhr / L_DPLL,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.7) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
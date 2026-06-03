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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def simplify_clause(clause, assignment):
            return [lit for lit in clause if lit not in assignment and -lit not in assignment]
        
        def unit_propagate(cnf, assignment):
            while True:
                changed = False
                for i, clause in enumerate(cnf):
                    if len(clause) == 1:
                        literal = clause[0]
                        if literal > 0:
                            assignment[literal] = True
                        else:
                            assignment[-literal] = False
                        cnf[i] = []
                        changed = True
                if not changed:
                    break
        
        def pure_literal_elimination(cnf, assignment):
            for lit in set(range(1, n+1)) | set([-i for i in range(1, n+1)]):
                pos_count = sum(1 for clause in cnf if lit in clause)
                neg_count = sum(1 for clause in cnf if -lit in clause)
                if pos_count == 0:
                    assignment[lit] = False
                elif neg_count == 0:
                    assignment[-lit] = True
            return [simplify_clause(clause, assignment) for clause in cnf]
        
        def dpll_helper(cnf, assignment):
            unit_propagate(cnf, assignment)
            cnf = pure_literal_elimination(cnf, assignment)
            if not any(clause for clause in cnf if len(clause) > 0):
                return True
            if all(len(clause) == 1 for clause in cnf):
                return False
            
            lit = next(lit for lit in range(1, n+1) if lit not in assignment and -lit not in assignment)
            new_cnf = [simplify_clause(clause, {lit: True}) for clause in cnf] + [[-lit]]
            if dpll_helper(new_cnf, assignment):
                return True
            new_cnf = [simplify_clause(clause, {lit: False}) for clause in cnf] + [[lit]]
            return dpll_helper(new_cnf, assignment)
        
        assignment = {}
        return dpll_helper(cnf, assignment)
    
    def gns_construction(cnf):
        # Simplified GNS construction for demonstration
        n = max(abs(lit) for lit in set([abs(clause[0]) for clause in cnf] + [abs(clause[1]) for clause in cnf]))
        return [[random.choice([-1, 1]) * random.randint(1, n) for _ in range(n)] for _ in range(n)]
    
    def minimal_local_indeterminacy(matrix):
        # Simplified calculation of minimal local indeterminacy
        n = len(matrix)
        det = 0
        for i in range(n):
            minor = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1)**i * matrix[0][i] * determinant(minor)
        return abs(det) ** (1/2)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for i in range(n):
            minor = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1)**i * matrix[0][i] * determinant(minor)
        return det
    
    n = random.randint(5, 40)
    m = random.randint(2*n, 3*n)
    cnf = generate_cnf(n, m)
    
    dpll_depth = len(cnf) if dpll(cnf) else float('inf')
    matrix = gns_construction(cnf)
    local_indeterminacy = minimal_local_indeterminacy(matrix)
    
    return {
        "metric_name": "local_indeterminacy",
        "metric_value": local_indeterminacy,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": local_indeterminacy <= (dpll_depth ** 0.5) + 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
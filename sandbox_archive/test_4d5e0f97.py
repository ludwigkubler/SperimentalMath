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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def unit_propagate(cnf, assignment):
            while True:
                found_unit_clause = False
                for clause in cnf:
                    if len([x for x in clause if x not in assignment]) == 1:
                        literal = [x for x in clause if x not in assignment][0]
                        assignment[literal] = 1 if literal > 0 else -1
                        found_unit_clause = True
                if not found_unit_clause:
                    break
            return assignment
        
        def dpll_helper(cnf, assignment):
            cnf = unit_propagate(cnf, assignment)
            if not cnf:
                return assignment
            if any(not any(l in assignment for l in clause) for clause in cnf):
                return None
            
            literal = next(l for l in range(1, len(cnf) + 1) if l not in assignment and -l not in assignment)
            assignment[literal] = 1
            result = dpll_helper(cnf, assignment)
            if result:
                return result
            assignment[literal] = -1
            result = dpll_helper(cnf, assignment)
            return result
        
        return dpll_helper(cnf, {})
    
    def quandle_rank(cnf):
        n = len(cnf)
        quandle = [[0 for _ in range(n)] for _ in range(n)]
        
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    i = literal - 1
                else:
                    i = -literal - 1
                for j in range(n):
                    if (i, j) not in quandle and (j, i) not in quandle:
                        quandle[i][j] = 1
        
        rank = 0
        for row in quandle:
            if sum(row) > rank:
                rank = sum(row)
        
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            denom = matrix[i][i]
            if denom == 0:
                continue
            
            for j in range(n):
                matrix[i][j] /= denom
            
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def dpll_length(cnf):
        assignment = {}
        stack = []
        clause_id = 0
        
        while True:
            unit_clause = next((c, i) for c in cnf if len([x for x in c if x not in assignment]) == 1)
            if unit_clause:
                literal, index = unit_clause
                assignment[literal] = 1 if literal > 0 else -1
                stack.append((literal, index))
                clause_id += 1
                continue
            
            if any(not any(l in assignment for l in c) for c in cnf):
                return len(stack)
            
            literal = next(l for l in range(1, len(cnf) + 1) if l not in assignment and -l not in assignment)
            assignment[literal] = 1
            stack.append((literal, clause_id))
            clause_id += 1
        
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = quandle_rank(cnf)
        length = dpll_length(cnf)
        results.append({"n": n, "rank": rank, "length": length})
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks = [r["rank"] for r in results]
    lengths = [r["length"] for r in results]
    
    mean_rank = sum(ranks) / len(ranks)
    mean_length = sum(lengths) / len(lengths)
    
    covariance = sum((ranks[i] - mean_rank) * (lengths[i] - mean_length) for i in range(len(ranks))) / len(ranks)
    variance_rank = sum((ranks[i] - mean_rank) ** 2 for i in range(len(ranks))) / len(ranks)
    variance_length = sum((lengths[i] - mean_length) ** 2 for i in range(len(lengths))) / len(lengths)
    
    correlation_coefficient = covariance / (math.sqrt(variance_rank) * math.sqrt(variance_length))
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) * math.sqrt(2 * (len(ranks) - 2)) / math.sqrt(2)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i, r) for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed[0]}")
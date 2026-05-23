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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        
        # Generate clauses for each variable
        for var in variables:
            clause = [var]
            for other_var in variables:
                if other_var != var:
                    clause.append(-other_var)
            clauses.append(clause)
        
        # Generate clauses for the OR of all variables
        or_clause = [-1] * n + list(range(1, n + 1))
        clauses.append(or_clause)
        
        return clauses
    
    def resolution_proof_length(clauses):
        stack = []
        while True:
            new_clauses = set()
            found_resolvent = False
            
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    clause_i = stack[i]
                    clause_j = stack[j]
                    
                    for lit_i in clause_i:
                        if -lit_i in clause_j:
                            resolvent = [l for l in clause_i if l != lit_i] + [l for l in clause_j if l != -lit_i]
                            new_clauses.add(tuple(sorted(resolvent)))
                            found_resolvent = True
            
            if not found_resolvent:
                break
            
            stack.extend(new_clauses)
        
        return len(stack)
    
    def noncommutative_rank(clauses):
        n = len(clauses[0])
        matrix = [[0] * n for _ in range(n)]
        
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    row, col = divmod(lit - 1, n)
                else:
                    row, col = divmod(-lit - 1, n)
                
                matrix[row][col] += 1
        
        # Gaussian elimination
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(rank)):
                continue
            
            pivot_row = rank
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    break
            
            if pivot_row != rank:
                matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
            
            for j in range(n):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] += factor * matrix[i][k]
        
        rank = sum(1 for row in matrix[:n] if any(row))
        return rank
    
    n = random.randint(5, 40)
    clauses = generate_tseitin_formula(n)
    
    resolution_length = resolution_proof_length(clauses)
    noncommutative_rank_value = noncommutative_rank(clauses)
    
    metric_name = "noncommutative_rank"
    metric_value = noncommutative_rank_value
    instances_tested = 1
    conjecture_holds = noncommutative_rank_value <= 2 * resolution_length
    counterexample = "" if conjecture_holds else f"n={n}, rank={noncommutative_rank_value}, resolution_length={resolution_length}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    total_rank = 0
    total_length = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={seed}")
            sys.exit(0)
        
        total_rank += trial_result["metric_value"]
        total_length += resolution_proof_length(generate_tseitin_formula(random.randint(5, 40)))
    
    mean_rank = total_rank / len(seeds)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in [run_trial(seed)["metric_value"] for seed in seeds]) / len(seeds))
    support_fraction = sum(run_trial(seed)["conjecture_holds"] for seed in seeds) / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
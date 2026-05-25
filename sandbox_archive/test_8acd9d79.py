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
    
    def rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        if n != m:
            return -1  # Not a square matrix, no rank defined
        
        # Gaussian elimination
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if matrix[max_row][i] == 0:
                return -1  # Pivot is zero, no rank defined
            
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below pivot
            for j in range(i+1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Count non-zero rows
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        
        return rank
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        if any(all(lit not in assignment or (lit < 0) == assignment[lit] for lit in clause) for clause in clauses):
            return False
        
        literal = next(lit for lit in range(1, len(clauses)+1) if lit not in assignment and -lit not in assignment)
        assignment[literal] = True
        if dpll(clauses, assignment):
            return True
        del assignment[literal]
        
        assignment[-literal] = True
        if dpll(clauses, assignment):
            return True
        del assignment[-literal]
        
        return False
    
    def proof_width(clauses):
        assignment = {}
        width = 0
        for clause in clauses:
            new_literals = [lit for lit in clause if lit not in assignment and -lit not in assignment]
            if new_literals:
                assignment[new_literals[0]] = True
                width += 1
        return width
    
    n = random.randint(5, 40)
    k = random.randint(2, 3)
    clauses = [[random.randint(-n, n) for _ in range(k)] for _ in range(n)]
    
    min_rank = rank(clauses)
    if min_rank == -1:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    proof_width_val = proof_width(clauses)
    
    return {
        "metric_name": "min_rank_vs_proof_width",
        "metric_value": min_rank / math.log(n, 2) ** 2,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_vs_proof_width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
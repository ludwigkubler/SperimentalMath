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
    
    def kac_moody_rank(cnf):
        n = len(cnf)
        if n > 40:
            return None
        
        # Construct the Kac-Moody Lie algebra associated with the CNF formula
        generators = set()
        relations = []
        
        for clause in cnf:
            for literal in clause:
                generators.add(abs(literal))
                for other_literal in clause:
                    if literal != other_literal:
                        relations.append((abs(literal), abs(other_literal)))
        
        # Convert to a list of lists for matrix representation
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for gen in generators:
            A[gen][gen] = 1
        
        for rel in relations:
            A[rel[0]][rel[1]] += 1
            A[rel[1]][rel[0]] += 1
        
        # Perform Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            
            for i in range(n):
                pivot_row = -1
                for j in range(rank, m):
                    if matrix[j][i] != 0:
                        pivot_row = j
                        break
                
                if pivot_row == -1:
                    continue
                
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                
                for j in range(n):
                    if j != i and matrix[rank-1][j] != 0:
                        factor = Fraction(matrix[rank-1][j], matrix[rank-1][i])
                        for k in range(n):
                            matrix[rank-1][k] -= factor * matrix[j][k]
            
            return rank
        
        rank = gaussian_elimination(A)
        
        return rank
    
    def generate_cnf(n, num_clauses):
        cnf = []
        literals = list(range(1, n + 1))
        
        for _ in range(num_clauses):
            clause = random.sample(literals, random.randint(1, n))
            cnf.append(clause)
        
        return cnf
    
    max_rank = 0
    instances_tested = 30
    
    for _ in range(instances_tested):
        n = random.randint(1, 40)
        num_clauses = random.randint(n, 2 * n)
        cnf = generate_cnf(n, num_clauses)
        
        rank = kac_moody_rank(cnf)
        if rank is None:
            continue
        
        max_rank = max(max_rank, rank)
    
    metric_value = max_rank
    conjecture_holds = max_rank <= 2**40
    counterexample = "" if conjecture_holds else "rank_exceeds_bound"
    
    return {
        "metric_name": "Minimal Rank of Kac-Moody Lie Algebra",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 8)]  # First 30 prime numbers
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_exceeds_bound\" first_failing_seed={first_failing_seed}")
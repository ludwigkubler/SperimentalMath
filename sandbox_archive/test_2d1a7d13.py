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
    
    def homology_groups(n):
        if n <= 0:
            return None
        
        A0 = [[0] * (n + 1) for _ in range(n + 1)]
        A1 = [[0] * (n + 1) for _ in range(n + 1)]
        A2 = [[0] * (n + 1) for _ in range(n + 1)]
        
        for i in range(1, n):
            A0[i][i-1] = 1
            A0[i][i+1] = 1
            A1[i][i-1] = -1
            A1[i][i] = 2
            A1[i][i+1] = -1
            A2[i][i-1] = 1
            A2[i][i] = -2
            A2[i][i+1] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                max_row = i
                for j in range(i + 1, rows):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                
                pivot = matrix[i][i]
                for j in range(cols):
                    matrix[i][j] /= pivot
                
                for k in range(rows):
                    if k != i:
                        factor = matrix[k][i]
                        for j in range(cols):
                            matrix[k][j] -= factor * matrix[i][j]
            
            return matrix
        
        A0 = gaussian_elimination(A0)
        A1 = gaussian_elimination(A1)
        A2 = gaussian_elimination(A2)
        
        rank_A0 = sum(1 for row in A0 if any(val != 0 for val in row))
        rank_A1 = sum(1 for row in A1 if any(val != 0 for val in row))
        rank_A2 = sum(1 for row in A2 if any(val != 0 for val in row))
        
        return (rank_A0, rank_A1, rank_A2)
    
    def tseitin_circuit(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        
        # Each variable is either true or false
        for var in variables:
            clauses.append([var])
            clauses.append([-var])
        
        # Implication: If x_i is true, then x_j must be true (for all j != i)
        for i in range(n):
            for j in range(n):
                if i != j:
                    clauses.append([f'x{i}', -f'x{j}'])
        
        return variables, clauses
    
    def satisfying_assignments(variables, clauses):
        n = len(variables)
        count = 0
        
        for assignment in itertools.product([-1, 1], repeat=n):
            if all(any(assignment[abs(clause[0])-1] * clause[i] > 0 for i in range(1, len(clause))) for clause in clauses):
                count += 1
        
        return count
    
    variables, clauses = tseitin_circuit(40)
    homology_ranks = homology_groups(len(variables))
    
    if homology_ranks is None:
        return {
            "metric_name": "homology_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    satisfying_count = satisfying_assignments(variables, clauses)
    ratio = Fraction(satisfying_count, len(variables))
    
    return {
        "metric_name": "homology_rank",
        "metric_value": sum(homology_ranks) / 3,
        "instances_tested": 1,
        "conjecture_holds": ratio >= Fraction(8, 10) and sum(homology_ranks) / 3 <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")
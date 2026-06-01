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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    k = 3
    
    m_min = max(k * 2, 1)
    m_max = min(n, 40)
    
    if m_max < m_min:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "m_max < m_min"
        }
    
    R_local_values = []
    S_clauses_values = []
    
    for _ in range(30):
        m = random.randint(m_min, m_max)
        
        # Generate a random k-SAT instance
        clause_set = set()
        while len(clause_set) < m:
            literals = [random.choice([f"x{i}", f"~x{i}"]) for i in range(1, n + 1)]
            clause = tuple(sorted(literals))
            if clause not in clause_set:
                clause_set.add(clause)
        
        # Construct the associated matroid
        matroid = []
        for clause in clause_set:
            row = [0] * n
            for literal in clause:
                var = int(literal[1:]) - 1
                if literal.startswith('x'):
                    row[var] = 1
                else:
                    row[var] = -1
            matroid.append(row)
        
        # Calculate the minimal local system rank R_local(G)
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                
                pivot = A[i][i]
                if pivot == 0:
                    continue
                
                for j in range(n):
                    A[i][j] /= pivot
                
                for j in range(m):
                    if j != i and A[j][i] != 0:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[i][k]
            
            rank = sum(1 for row in A if any(row))
            return rank
        
        R_local = gaussian_elimination(matroid)
        
        # Measure the clause set complexity S_clauses(m)
        S_clauses = len(clause_set)
        
        R_local_values.append(R_local)
        S_clauses_values.append(S_clauses)
    
    n_max = max(len(clause) for clause in clause_set)
    
    if n_max < 16:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(R_local_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    # Compute the Pearson correlation coefficient
    mean_R = sum(R_local_values) / len(R_local_values)
    mean_S = sum(S_clauses_values) / len(S_clauses_values)
    
    cov = sum((R_local - mean_R) * (S_clauses - mean_S) for R_local, S_clauses in zip(R_local_values, S_clauses_values)) / len(R_local_values)
    var_R = sum((R_local - mean_R) ** 2 for R_local in R_local_values) / len(R_local_values)
    var_S = sum((S_clauses - mean_S) ** 2 for S_clauses in S_clauses_values) / len(S_clauses_values)
    
    if var_R == 0 or var_S == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(R_local_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "variance of R_local or S_clauses is zero"
        }
    
    pearson_corr = cov / (var_R * var_S)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(R_local_values),
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
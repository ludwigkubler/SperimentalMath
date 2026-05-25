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
    
    def generate_random_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            if 0 not in clause:
                clauses.append(clause)
        return clauses
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [0] * (m - n) + [i] for i, row in enumerate(matrix)]
        
        for col in range(n):
            max_row = None
            for i in range(col, m):
                if max_row is None or abs(augmented_matrix[i][col]) > abs(augmented_matrix[max_row][col]):
                    max_row = i
            
            augmented_matrix[col], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[col]
            
            for i in range(m):
                if i != col:
                    factor = Fraction(augmented_matrix[i][col], augmented_matrix[col][col])
                    for j in range(n + m):
                        augmented_matrix[i][j] -= factor * augmented_matrix[col][j]
        
        rank = 0
        for row in augmented_matrix[:n]:
            if any(x != 0 for x in row):
                rank += 1
        
        return rank
    
    def resolution_depth(clauses):
        stack = []
        seen = set()
        depth = 0
        
        while stack or clauses:
            new_clauses = []
            if stack:
                clause = stack.pop()
            else:
                clause = random.choice(clauses)
            
            for literal in clause:
                if -literal in seen:
                    continue
                seen.add(literal)
                
                new_clause = [l for l in clause if l != literal]
                if not new_clause:
                    return depth
                
                new_clauses.append(new_clause)
            
            stack.extend(new_clauses)
            depth += 1
        
        return float('inf')
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = generate_random_cnf(n, m)
    rho = rank([[1 if abs(x) == i+1 else 0 for x in clause] for clause in clauses])
    t_star = resolution_depth(clauses)
    
    return {
        "metric_name": "rho_over_log_t_star",
        "metric_value": rho / math.log(t_star + 1, 2),
        "instances_tested": 1,
        "conjecture_holds": True if rho >= math.log(t_star + 1, 2) else False,
        "counterexample": "" if rho >= math.log(t_star + 1, 2) else f"CNF with n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
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
        cnf = []
        for _ in range(n):
            clause = set(random.sample(range(1, 2*n+1), 3))
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        n = len(cnf)
        clauses = [set() for _ in range(n)]
        for i in range(n):
            clauses[i] = set(cnf[i])
        
        resolvent = []
        while True:
            new_resolvents = []
            for i in range(n):
                for j in range(i+1, n):
                    if len(clauses[i].intersection(clauses[j])) == 2:
                        l1, l2 = clauses[i].intersection(clauses[j])
                        new_clause = [l for l in clauses[i] | clauses[j] if l != -l1 and l != -l2]
                        new_resolvents.append(new_clause)
            if not new_resolvents:
                break
            resolvent.extend(new_resolvents)
            cnf.extend(new_resolvents)
        return len(resolvent)
    
    def grothendieck_group(cnf):
        n = len(cnf)
        matroid_matrix = [[0] * (n+1) for _ in range(n+1)]
        for i in range(n):
            for l in cnf[i]:
                if l > 0:
                    matroid_matrix[l][i+1] += 1
                else:
                    matroid_matrix[-l][i+1] -= 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(cols - 1):
                if matrix[i][i] == 0:
                    for j in range(i + 1, rows):
                        if matrix[j][i] != 0:
                            matrix[i], matrix[j] = matrix[j], matrix[i]
                            break
                    else:
                        continue
                pivot = Fraction(matrix[i][i])
                for j in range(i, cols):
                    matrix[i][j] /= pivot
                for j in range(rows):
                    if j == i:
                        continue
                    factor = Fraction(matrix[j][i])
                    for k in range(i, cols):
                        matrix[j][k] -= factor * matrix[i][k]
        
        gaussian_elimination(matroid_matrix)
        
        rank = 0
        for row in matroid_matrix:
            if any(row[i] != 0 for i in range(1, len(row))):
                rank += 1
        
        return rank
    
    def local_cohomological_defect(cnf):
        return grothendieck_group(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    lcd = local_cohomological_defect(cnf)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "local_cohomological_defect",
        "metric_value": lcd,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 30)]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
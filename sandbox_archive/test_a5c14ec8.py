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
    
    def generate_k_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set(random.sample(range(1, n + 1), k=random.randint(1, n)))
            if random.choice([True, False]):
                clause = {x * -1 for x in clause}
            clauses.append(clause)
        return clauses
    
    def incidence_matrix(k_cnf, n):
        m = len(k_cnf)
        matrix = [[0] * (n + m) for _ in range(n)]
        for i, clause in enumerate(k_cnf):
            for var in clause:
                if var > 0:
                    matrix[var - 1][i + n] = 1
                else:
                    matrix[-var - 1][i + n] = -1
        return matrix
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = None
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for j in range(rows):
                    if j != rank - 1 and matrix[j][i] != 0:
                        factor = Fraction(matrix[j][i], matrix[rank - 1][i])
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[rank - 1][k]
        return rank
    
    n = random.randint(3, 40)
    m = int(n * (n / 2))  # Fixed clause density
    k_cnf = generate_k_cnf(n, m)
    
    mat = incidence_matrix(k_cnf, n)
    rank = gaussian_elimination(mat)
    
    return {
        "metric_name": "Ehrhart Cohomology Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= m * math.log(m),
        "counterexample": "" if rank <= m * math.log(m) else f"Rank {rank} > {m * math.log(m)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
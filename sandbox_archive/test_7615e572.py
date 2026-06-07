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
        for _ in range(10 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if rank < m:
                pivot_row = rank
                while A[pivot_row][i] == 0 and pivot_row < m - 1:
                    pivot_row += 1
                if A[pivot_row][i] != 0:
                    A[rank], A[pivot_row] = A[pivot_row], A[rank]
                    for j in range(i + 1, n):
                        factor = -A[rank][j] / A[rank][i]
                        for k in range(rank, m):
                            A[k][j] += factor * A[k][i]
                    rank += 1
                else:
                    continue
            else:
                break
        return rank
    
    def resolution_width(clauses):
        queue = clauses[:]
        visited = set()
        while queue:
            clause = queue.pop(0)
            for literal in clause:
                neg_literal = -literal
                if neg_literal in visited:
                    continue
                visited.add(neg_literal)
                new_clause = []
                for other_clause in queue:
                    if neg_literal in other_clause:
                        new_clause.extend([l for l in other_clause if l != neg_literal])
                    else:
                        queue.append(other_clause)
                if not new_clause:
                    return len(queue) + 1
                queue.append(new_clause)
        return float('inf')
    
    def toric_variants(clauses):
        m, n = len(clauses), len(clauses[0])
        A = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if clauses[i][j] > 0:
                    A[i][j] = 1
                else:
                    A[i][j] = -1
            A[i][-1] = 1
        
        rank = gaussian_elimination(A)
        return m - rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            M_phi = toric_variants(cnf)
            w_phi = resolution_width(cnf)
            
            if M_phi > w_phi + 10:
                conjecture_holds = False
                counterexample = f"n={n}, Mφ={M_phi}, w(φ)={w_phi}"
                break
            
            total_metric_value += M_phi * w_phi
            instances_tested += 1
            n_max = max(n_max, n)
    
    return {
        "metric_name": "Mφ * w(φ)",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
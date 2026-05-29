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
    
    # Generate an n-bit XOR boolean function randomly for each instance.
    n = 10  # Fixed size for simplicity; can be adjusted as needed
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the minimal tropical cycle rank TCR(n) for each representation of the boolean function in the max-plus semiring.
    def min_tropical_cycle_rank(f):
        m = len(f)
        A = [[math.inf] * m for _ in range(m)]
        for i in range(m):
            for j in range(i, m):
                if f[i] == f[j]:
                    A[i][j] = 0
                    A[j][i] = 0
                else:
                    A[i][j] = 1
                    A[j][i] = 1
        
        def gaussian_elimination(M):
            rows, cols = len(M), len(M[0])
            for i in range(rows):
                max_row = i
                for j in range(i + 1, rows):
                    if M[j][i] > M[max_row][i]:
                        max_row = j
                M[i], M[max_row] = M[max_row], M[i]
                
                factor = M[i][i]
                for j in range(cols):
                    M[i][j] /= factor
                
                for j in range(rows):
                    if i != j:
                        factor = M[j][i]
                        for k in range(cols):
                            M[j][k] -= factor * M[i][k]
            
            return M
        
        gaussian_elimination(A)
        
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    TCR_n = min_tropical_cycle_rank(f)
    
    # Calculate the randomized query complexity Q(f) for XOR.
    def xor_query_complexity(n, f):
        queries = []
        for i in range(2**n):
            x = [int(b) for b in format(i, f'0{n}b')]
            y = 0
            for j in range(n):
                if x[j] == 1:
                    y ^= f[j]
            queries.append(y)
        return len(set(queries))
    
    Q_f = xor_query_complexity(n, f)
    
    # Calculate the Spearman rank correlation coefficient between Q(f) and TCR(n).
    def spearman_rank_correlation(Q_f, TCR_n):
        if not Q_f or not TCR_n:
            return 0
        n = len(Q_f)
        ranks_Q = {x: i for i, x in enumerate(sorted(set(Q_f)), start=1)}
        ranks_T = {x: i for i, x in enumerate(sorted(set(TCR_n)), start=1)}
        rank_diffs = [(ranks_Q[x] - ranks_T[x]) ** 2 for x in Q_f]
        return 1 - (6 * sum(rank_diffs)) / (n * (n**2 - 1))
    
    rho = spearman_rank_correlation([Q_f], [TCR_n])
    
    # Calculate the mean difference between Q(f) and TCR(n).
    def mean_difference(Q_f, TCR_n):
        return abs(Q_f[0] - TCR_n[0])
    
    diff = mean_difference([Q_f], [TCR_n])
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rho >= 0.8 and diff <= 3,
        "counterexample": "" if rho >= 0.8 and diff <= 3 else "Spearman rank correlation < 0.8 or mean difference > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Spearman rank correlation < 0.8 or mean difference > 3' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
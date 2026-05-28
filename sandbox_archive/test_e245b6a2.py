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
    
    def is_symmetric(f):
        for x in range(1 << n):
            if f(x) != f(x ^ ((1 << (n - 1)) - 1)):
                return False
        return True
    
    def generate_random_symmetric_function(n):
        while True:
            f = [random.randint(0, 1) for _ in range(1 << n)]
            if is_symmetric(f):
                return f
    
    def syntactic_monoid(f):
        monoid = set()
        for x in range(1 << n):
            for y in range(1 << n):
                z = 0
                for i in range(n):
                    if (x & (1 << i)) and (y & (1 << i)):
                        z |= f[i]
                monoid.add(z)
        return monoid
    
    def quandle_operation(M, a, b):
        result = set()
        for x in M:
            for y in M:
                z = 0
                for i in range(n):
                    if (x & (1 << i)) and (y & (1 << i)):
                        z |= a[i]
                    else:
                        z |= b[i]
                result.add(z)
        return result
    
    def rank(M):
        rows, cols = len(M), len(M[0])
        matrix = [[M[i][j] for j in range(cols)] for i in range(rows)]
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                
                if A[i][i] == 0:
                    continue
                
                for j in range(i + 1, m):
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
            
            rank = sum(1 for row in A if any(row))
            return rank
        
        return gaussian_elimination(matrix)
    
    def communication_complexity(f):
        # Simplified model: each bit requires 1 bit of communication
        return n
    
    n_values = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
    total_metric = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_random_symmetric_function(n)
        M = syntactic_monoid(f)
        neg_f = [1 - x for x in f]
        neg_M = syntactic_monoid(neg_f)
        
        min_rank = float('inf')
        for a in range(1 << n):
            for b in range(1 << n):
                Q = quandle_operation(M, a, b)
                rank_Q = rank(Q)
                if rank_Q < min_rank:
                    min_rank = rank_Q
        
        metric_value = min_rank
        total_metric += metric_value
        instances_tested += 1
    
    mean_metric = total_metric / instances_tested
    support_fraction = sum(1 for n in n_values if min_rank <= n / math.log(n)) / len(n_values)
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={n}, min_rank={min_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={r['instances_tested']}, min_rank={r['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
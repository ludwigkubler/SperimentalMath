# auto-injected by SEC sandbox
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def memoized_recursive_query_enumeration(f, n):
        @lru_cache(None)
        def query(x):
            if x == 0:
                return 1
            else:
                return sum(query((x >> i) ^ (x & -x)) for i in range(n)) % 2
        return query
    
    def build_lifted_communication_matrix(f, n, b):
        M = [[f(tuple(x[i:i+b] for i in range(0, len(x), b))) for x in product([0, 1], repeat=n)] for y in product([0, 1], repeat=n)]
        return M
    
    def build_bipartite_graph_laplacian(M):
        n = int(math.log2(len(M)))
        L = [[0] * (n * b) for _ in range(n * b)]
        for i in range(n * b):
            for j in range(n * b):
                if M[i // b][j // b] == 1:
                    L[i][j] = -1
                    if i != j:
                        L[j][i] = 1
        return L
    
    def determinant(M, mod=604853):
        n = len(M)
        det = 1
        for i in range(n):
            pivot = M[i][i]
            for j in range(i + 1, n):
                factor = M[j][i] * pow(pivot, -1, mod) % mod
                for k in range(i, n):
                    M[j][k] = (M[j][k] - factor * M[i][k]) % mod
            det = det * pivot % mod
        return det
    
    def fraction_free_bareiss(M):
        n = len(M)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, row in enumerate(M):
            A[i][i] = 1
            for j, val in enumerate(row):
                A[i][j + n + 1] = val
        det = 0
        for k in range(1, n + 1):
            pivot = A[k - 1][k - 1]
            for i in range(k, n + 1):
                for j in range(k, n + 1):
                    A[i][j] = (A[i][j] * pivot - A[i - 1][j] * A[k - 1][i]) % mod
            det = A[n][n]
        return det
    
    def spanning_tree_count(L):
        n = len(L)
        L_mod_2 = [[(x + y) % 2 for x, y in zip(row[:n], row[n:])] for row in L]
        det = fraction_free_bareiss(L_mod_2)
        if det == 0:
            return 0
        else:
            return det
    
    def parity_function(n):
        return lambda x: sum(x) % 2
    
    n_values = [1, 2, 3]
    b_values = [2, 3]
    results = []
    
    for n in n_values:
        for b in b_values:
            if n <= 2:
                f_values = list(product([0, 1], repeat=2**n))
            else:
                f_values = random.sample(list(product([0, 1], repeat=2**n)), 200)
            
            for f in f_values:
                query = memoized_recursive_query_enumeration(lambda x: f[x], n)
                d = query(0)
                
                M = build_lifted_communication_matrix(f, n, b)
                L = build_bipartite_graph_laplacian(M)
                tau = spanning_tree_count(L)
                
                if tau == 0:
                    continue
                
                log_tau = math.log2(tau)
                lower_bound = d * 2**(b*n - 2)
                slack = abs(log_tau - lower_bound)
                
                result = {
                    "metric_name": "log2_tau",
                    "metric_value": log_tau,
                    "instances_tested": 1,
                    "conjecture_holds": slack <= b and (slack == 0 or f != parity_function(n)),
                    "counterexample": "" if slack <= b else f"n={n}, b={b}"
                }
                results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric_value": mean_metric_value,
        "std_metric_value": std_metric_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))
    
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["mean_metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\", first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
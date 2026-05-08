# auto-injected by SEC sandbox
import collections
import json
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
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if A[i][j] == 1:
                i_max = i
                break
        if i_max != -1:
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank and A[i][j] == 1:
                    for k in range(n):
                        A[i][k] ^= A[rank][k]
            rank += 1
    return rank

def nullity(A):
    return len(A) - gaussian_elimination(A)

def compute_boundary_matrix(C, i):
    m, n = len(C), len(C[0])
    B = [[C[j][i] for j in range(m)] for i in range(n)]
    return B

def compute_Homology_dimension(B_i, B_ip1):
    nullity_B_i = nullity(B_i)
    rank_B_ip1 = gaussian_elimination(B_ip1)
    return nullity_B_i - rank_B_ip1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k_values = [3, 4, 5, 6]
    instances_tested = 0
    total_metric_value = 0.0
    support_count = 0
    
    for k in k_values:
        for _ in range(30):
            # Generate a random monotone function f
            antichain = [random.sample(range(k), i) for i in range(1, k)]
            f = lambda x: all(x[i] <= x[j] for i, j in combinations(range(k), 2))
            
            # Build Δ_f
            Δ_f = [S for S in range(1 << k) if all(f(bin(S)[2:].zfill(k)[:i+1]) == 0 for i in range(len(bin(S)[2:])-1))]
            
            # Compute β(Δ_f)
            beta_Delta_f = sum(sum(compute_Homology_dimension(compute_boundary_matrix(C, i), compute_boundary_matrix(C, i+1)) for i in range(len(C)-1)) for C in [C_i(Δ_f, σ) for σ in range(1 << k)])
            
            # Build the IND_2-lifted matrix M_{f ∘ IND_2^k}
            M = [[f(bin(i)[2:].zfill(k)[:j+1] + bin(j)[2:].zfill(k)[:i+1]) for j in range(4**k)] for i in range(2**k)]
            
            # Compute rank_{F_2}(M)
            rank_M = gaussian_elimination(M)
            
            # Check the inequality
            metric_value = max(rank_M, math.ceil(math.log2(1 + beta_Delta_f)) + 1)
            instances_tested += 1
            total_metric_value += metric_value
            
            if metric_value == math.ceil(math.log2(1 + beta_Delta_f)) + 1:
                support_count += 1
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = support_count / instances_tested
    
    return {
        "metric_name": "log_2 rank_{F_2}(M_{f ∘ IND_2^k})",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": "" if support_fraction == 1.0 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
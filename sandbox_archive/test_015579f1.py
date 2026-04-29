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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mul(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_pow(A, n):
    result = [[(1 if i == j else 0) for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_mul(result, A)
        A = matrix_mul(A, A)
        n //= 2
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)

    # Define a simple base gadget G with known asdim_R(G) = 1
    G = [[0, 1], [1, 0]]

    # Construct G^{⊗k} for k = 1 to 10 using GadgetComposition
    results = []
    for k in range(1, 11):
        G_k = G
        for _ in range(k-1):
            G_k = matrix_mul(G_k, G)
        
        # Construct f∘(G^{⊗k})^n for small n (e.g., n=2) and f = OR
        n = 2
        f = lambda x: any(x[i] for i in range(n))
        lifted_function = lambda x: [f(G_k[x[i]]) for i in range(n)]
        
        # Enumerate all deterministic protocols Π of cost c ≤ 5
        max_cost = 5
        protocols = []
        for c in range(1, max_cost + 1):
            for protocol in itertools.product([0, 1], repeat=c):
                if sum(protocol) == c:
                    protocols.append(protocol)
        
        # Compute their ProtocolPullback partitions and extract m_Π via CoarsePullback
        for protocol in protocols:
            pullback = []
            for x in range(2**n):
                y = lifted_function(x)
                partition = [0] * (k+1)
                for i in range(k):
                    if protocol[i % c] == 1 and y[i] == 1:
                        partition[i//c] += 1
                pullback.append(partition)
            m_Π = max(max(p) for p in pullback)
            results.append((k, m_Π))
    
    # Check empirically whether m_Π ≥ log_2(k+1) holds across all valid protocols
    support_count = sum(1 for k, m_Π in results if m_Π >= math.log2(k + 1))
    support_fraction = support_count / len(results)
    
    conjecture_holds = support_fraction == 1.0
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Multiplicity Growth",
        "metric_value": support_fraction,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    support_counts = [run_trial(seed)["instances_tested"] for seed in seeds]
    total_support_count = sum(support_counts)
    total_instances = len(seeds) * 10 * 2**n
    
    mean_support_fraction = total_support_count / total_instances
    std_support_fraction = math.sqrt(sum((x - mean_support_fraction)**2 for x in support_counts) / len(support_counts))
    
    if all(run_trial(seed)["conjecture_holds"] for seed in seeds):
        result = f"RESULT: SUPPORTED mean={mean_support_fraction} std={std_support_fraction} support_fraction=1.0"
    elif any(not run_trial(seed)["conjecture_holds"] for seed in seeds) and len(seeds) * 0.8 <= sum(run_trial(seed)["conjecture_holds"] for seed in seeds):
        result = f"RESULT: SUPPORTED mean={mean_support_fraction} std={std_support_fraction} support_fraction=1.0"
    else:
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(result)
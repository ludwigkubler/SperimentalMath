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
    n = 40
    random.seed(seed)
    
    def generate_transition_matrix(n):
        P = [[random.random() for _ in range(2)] for _ in range(2**n)]
        return P
    
    def noncommutative_fourier_transform(P, g):
        F_P = [[0] * 2 for _ in range(2)]
        for x in range(2**n):
            F_P[0][0] += P[x][0] * g(x)
            F_P[1][1] += P[x][1] * g(x)
        return F_P
    
    def operator_norm(F_P):
        norm = 0
        for i in range(2):
            for j in range(2):
                norm += abs(F_P[i][j])
        return norm
    
    def trivial_bp(n):
        return [[1, 0] for _ in range(2**n)]
    
    def ip_2_bp(n):
        P = [[0, 0] for _ in range(2**n)]
        for x in range(2**n):
            if bin(x).count('1') % 2 == 0:
                P[x][0] = 1
            else:
                P[x][1] = 1
        return P
    
    def g(x):
        return (-1)**x
    
    P_trivial = trivial_bp(n)
    P_ip_2 = ip_2_bp(n)
    
    norm_trivial = operator_norm(noncommutative_fourier_transform(P_trivial, g))
    norm_ip_2 = operator_norm(noncommutative_fourier_transform(P_ip_2, g))
    
    return {
        "metric_name": "operator_norm",
        "metric_value": norm_ip_2 / norm_trivial,
        "instances_tested": 1,
        "conjecture_holds": True if norm_ip_2 > n * norm_trivial else False,
        "counterexample": "" if norm_ip_2 > n * norm_trivial else "trivial_bp"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='trivial_bp' first_failing_seed={first_failing_seed}")
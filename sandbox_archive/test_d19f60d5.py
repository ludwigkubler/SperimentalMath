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

import math
import random

def hamming_weight(x):
    return bin(x).count('1')

def xor(x, y):
    return x ^ y

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 8, 11, 14]
    results = []
    
    for n in n_values:
        X_f = [(i << n) | j for i in range(1 << n) for j in range(1 << n)]
        f = lambda x: xor(x >> n, x & ((1 << n) - 1))
        
        d_f = [[math.log2(hamming_weight(xor(x, y))) for y in X_f] for x in X_f]
        c_IP = [[(-1) ** f(xor(x, y)) if d_f[x][y] <= math.log2(2 * n) else 0 for y in range(len(X_f))] for x in range(len(X_f))]
        
        p_R_values = []
        for R in range(1, int(math.log2(2 * n)) + 1):
            T_R = [[1 if d_f[x][y] <= R else 0 for y in range(len(X_f))] for x in range(len(X_f))]
            ball_volume = sum(sum(row) for row in T_R)
            T_R = [[t / ball_volume for t in row] for row in T_R]
            p_R = sum(c_IP[x][y] * T_R[x][y] for x in range(len(X_f)) for y in range(len(X_f)))
            p_R_values.append(math.log(abs(p_R)))
        
        alpha_n = (p_R_values[-1] - p_R_values[0]) / math.log2(2 * n)
        results.append({"n": n, "alpha_n": alpha_n})
    
    return {
        "metric_name": "alpha_n",
        "metric_value": sum(result["alpha_n"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["alpha_n"] >= 0.7 for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
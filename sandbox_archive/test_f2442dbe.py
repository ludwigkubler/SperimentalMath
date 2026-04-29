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
    
    def generate_read_twice_bp(n):
        bp = []
        for i in range(2**n):
            row = [random.choice(range(2)) for _ in range(n)]
            bp.append(row)
        return bp
    
    def transition_matrix(bp):
        n = len(bp[0])
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(n):
                if bp[i][j] == 1:
                    M[i][i ^ (1 << j)] += 1
        return M
    
    def r_transform(M):
        n = len(M)
        R = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    R[i][j] = Fraction(1, 2) * (M[i][i] + M[j][j])
                else:
                    R[i][j] = Fraction(M[i][j], 2)
        return R
    
    def free_entropy(R):
        n = len(R)
        det_R = 1
        for i in range(n):
            det_R *= R[i][i]
        return -math.log(det_R, 2)
    
    n = 40
    read_twice_bp = generate_read_twice_bp(n)
    read_twice_matrix = transition_matrix(read_twice_bp)
    R = r_transform(read_twice_matrix)
    rho = free_entropy(R)
    
    trivial_rho = math.log(n)
    
    return {
        "metric_name": "free_entropy",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": rho >= trivial_rho - 0.1 and rho <= trivial_rho + 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"free_entropy_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
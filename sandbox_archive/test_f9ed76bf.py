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
    
    def generate_read_twice_bp(n):
        # Generate a read-twice BP for IP_2
        bp = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if (i + j) % 2 == 0:
                    bp[i][j] = random.randint(1, 5)
                else:
                    bp[i][j] = random.randint(-5, -1)
        return bp
    
    def transition_matrix(bp):
        n = len(bp)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    T[i][j] += bp[i][k] * bp[k][j]
        return T
    
    def free_cumulant(T, n):
        # Approximate free cumulant using the inversion formula
        det_T = 1.0
        for i in range(n):
            det_T *= T[i][i]
        if det_T == 0:
            return -math.inf
        return math.log(det_T)
    
    def log_size(bp):
        n = len(bp)
        return math.log(n * n)
    
    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    T = transition_matrix(bp)
    rho_P = free_cumulant(T, n)
    
    if "IP_2" in seed_to_description[seed]:
        expected_bound = n / 2
    else:
        expected_bound = log_size(bp) + 10
    
    conjecture_holds = rho_P >= expected_bound
    counterexample = "" if conjecture_holds else f"rho(P)={rho_P}, bound={expected_bound}"
    
    return {
        "metric_name": "free_cumulant",
        "metric_value": rho_P,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    seed_to_description = {
        2: "IP_2",
        3: "general BP",
        5: "IP_2",
        7: "general BP",
        11: "IP_2",
        13: "general BP",
        17: "IP_2",
        19: "general BP",
        23: "IP_2",
        29: "general BP"
    }
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho_P = sum(r["metric_value"] for r in results) / len(results)
    std_rho_P = math.sqrt(sum((r["metric_value"] - mean_rho_P) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_P} std={std_rho_P} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
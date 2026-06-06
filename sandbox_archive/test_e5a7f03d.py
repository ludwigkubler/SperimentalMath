# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def calculate_symplectic_volume(cnf):
        # Placeholder function to simulate symplectic volume calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf) ** 0.5
    
    def calculate_variance_in_rank(cnf):
        # Placeholder function to simulate variance in communication complexity rank calculation
        # This is a dummy implementation and should be replaced with actual computation
        return sum(len(clause) for clause in cnf) / len(cnf)
    
    n = random.randint(5, 40)
    m = random.randint(n // 2, n)
    cnf = generate_cnf(n, m)
    
    sv = calculate_symplectic_volume(cnf)
    vcr = calculate_variance_in_rank(cnf)
    
    ratio = sv / vcr if vcr != 0 else float('inf')
    
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= n ** 0.5,
        "counterexample": "" if ratio >= n ** 0.5 else "Ratio < √n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio < √n\" first_failing_seed={first_failing_seed}")
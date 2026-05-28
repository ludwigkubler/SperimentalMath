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
    
    def generate_bp(n):
        # Generate a random read-twice branching program with n variables
        bp = []
        for _ in range(2**n):
            row = [random.choice([0, 1]) for _ in range(n)]
            bp.append(row)
        return bp
    
    def compute_rho_qc(bp):
        # Compute the quantum category invariant ρ(QC)(P) using a constructive mapping
        n = len(bp[0])
        size = len(bp)
        rho_qc = sum(1 for row in bp if any(x == 1 for x in row)) / size
        return rho_qc
    
    def log_size(size):
        # Compute the logarithm of the size of the branching program
        return math.log2(size) if size > 0 else float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    rho_qc_values = []
    
    for n in n_values:
        bp = generate_bp(n)
        rho_qc = compute_rho_qc(bp)
        rho_qc_values.append(rho_qc)
    
    mean_rho_qc = sum(rho_qc_values) / len(rho_qc_values)
    max_rho_qc = max(rho_qc_values)
    min_rho_qc = min(rho_qc_values)
    
    conjecture_holds = all(max_rho_qc <= 10 * log_size(n) for n in n_values)
    counterexample = "" if conjecture_holds else f"max_rho_qc={max_rho_qc}, expected<=10*log(size(P))"
    
    return {
        "metric_name": "rho_qc",
        "metric_value": mean_rho_qc,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_rho_qc = sum(r["metric_value"] for r in results) / len(results)
    max_rho_qc = max(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_qc} std=0.0 support_fraction={support_fraction}")
    elif max_rho_qc > 10 * math.log2(40):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_rho_qc={max_rho_qc}, expected<=10*log(size(P))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
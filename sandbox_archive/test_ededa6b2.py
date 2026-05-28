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
    
    def construct_sheaf(f):
        n = len(f)
        sheaf = []
        for i in range(n):
            row = [f[j] if j & (1 << i) else 0 for j in range(2**n)]
            sheaf.append(row)
        return sheaf
    
    def compute_minimal_rank(sheaf):
        n = len(f)
        m = len(sheaf)
        A = [[Fraction(sheaf[i][j]) for j in range(m)] for i in range(n)]
        
        # Gaussian elimination
        for i in range(n):
            if A[i][i] == 0:
                return float('inf')  # Singular matrix, minimal rank is infinite
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(m):
                    A[j][k] -= factor * A[i][k]
        
        # Count non-zero rows
        minimal_rank = sum(1 for row in A if any(row))
        return minimal_rank
    
    def compute_acc0_circuit_weight(f):
        n = len(f)
        weight = 0
        for i in range(n):
            if f[i] == 1:
                weight += 1
        return weight
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_weight = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            f = [random.randint(0, 1) for _ in range(2**n)]
            sheaf = construct_sheaf(f)
            minimal_rank = compute_minimal_rank(sheaf)
            acc0_weight = compute_acc0_circuit_weight(f)
            
            if minimal_rank == float('inf'):
                continue
            
            total_rank += minimal_rank
            total_weight += acc0_weight
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = total_rank / instances_tested
    mean_weight = total_weight / instances_tested
    
    if math.log(n) <= mean_rank <= 2 * math.log(n):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"minimal rank {mean_rank} not in range [log({n}), 2*log({n})]"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rank = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    instances_tested = sum(r["instances_tested"] for r in results)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank/instances_tested} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")
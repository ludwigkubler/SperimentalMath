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
    
    n = 10  # Start with a small size and increase if needed
    
    def generate_matrix(n):
        M = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        return M
    
    def matrix_rank(M):
        m, n = len(M), len(M[0])
        rank = 0
        A = [row[:] for row in M]
        
        for i in range(min(m, n)):
            if A[i][i] == 0:
                swap_found = False
                for j in range(i + 1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
            
            rank += 1
        
        return rank
    
    def simulate_disjointness(n):
        bits = [random.choice([0, 1]) for _ in range(n)]
        communication_cost = n  # Simplified model
        return communication_cost
    
    M = generate_matrix(n)
    r_M = matrix_rank(M)
    comm_complexity = simulate_disjointness(n)
    
    if comm_complexity < 2 * r_M:
        return {
            "metric_name": "communication_complexity",
            "metric_value": comm_complexity,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"r(M)={r_M}, comm_complexity={comm_complexity}"
        }
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_comm_complexity = 0
    total_instances = 0
    support_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_comm_complexity += trial_result["metric_value"]
        total_instances += trial_result["instances_tested"]
        if trial_result["conjecture_holds"]:
            support_count += 1
    
    mean_comm_complexity = total_comm_complexity / total_instances
    std_comm_complexity = math.sqrt(sum((x - mean_comm_complexity) ** 2 for x in [trial_result["metric_value"] for trial_result in results]) / len(results))
    support_fraction = support_count / len(seeds)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, trial_result in zip(seeds, results) if not trial_result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='r(M)<2*comm_complexity' first_failing_seed={first_failing_seed}")
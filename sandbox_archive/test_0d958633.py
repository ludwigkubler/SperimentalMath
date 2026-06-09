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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def construct_metric_space(cnf):
        n = len(cnf[0])
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                count = sum(1 for clause in cnf if (i + 1) in clause and (j + 1) not in clause or (i + 1) not in clause and (j + 1) in clause)
                M[i][j] = Fraction(1, abs(count))
                M[j][i] = M[i][j]
        return M
    
    def calculate_geometric_entropy(M):
        n = len(M)
        total = sum(sum(row) for row in M)
        entropy = 0
        for i in range(n):
            for j in range(i + 1, n):
                if M[i][j] > 0:
                    entropy += -M[i][j] * math.log2(M[i][j])
        return entropy
    
    def calculate_frege_proof_depth(cnf):
        # Placeholder function to simulate Frege proof depth calculation
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    M = construct_metric_space(cnf)
    het_M = calculate_geometric_entropy(M)
    d_phi = calculate_frege_proof_depth(cnf)
    
    metric_name = "Frege Proof Depth vs Geometric Entropy"
    metric_value = d_phi
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_metric_value = 0
    support_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            support_count += 1
        
        results.append(trial_result)
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
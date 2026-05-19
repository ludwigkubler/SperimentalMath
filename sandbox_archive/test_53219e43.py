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
        for _ in range(n):
            layer = [random.choice([0, 1]) for _ in range(2)]
            bp.append(layer)
        return bp
    
    def transition_matrix(bp):
        n = len(bp)
        T = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if bp[i][0] == bp[j][1]:
                    T[i][j+1] += 1
                else:
                    T[i][j] += 1
        return T
    
    def free_entropy(T):
        n = len(T) - 1
        R = [[Fraction(0, 1)] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            total = sum(T[i])
            if total == 0:
                continue
            for j in range(n + 1):
                R[j][i] = Fraction(T[i][j], total)
        
        entropy = 0
        for i in range(n + 1):
            for j in range(n + 1):
                if R[j][i] != 0:
                    entropy += R[j][i] * math.log(R[j][i])
        return -entropy
    
    def is_ip2(bp):
        n = len(bp)
        for i in range(n):
            if bp[i][0] != bp[(i + 1) % n][1]:
                return False
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    rho_ip2_total = 0
    rho_non_ip2_total = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different BPs
            bp = generate_read_twice_bp(n)
            if is_ip2(bp):
                rho_ip2_total += free_entropy(transition_matrix(bp))
            else:
                rho_non_ip2_total += free_entropy(transition_matrix(bp))
            instances_tested += 1
    
    rho_ip2_avg = rho_ip2_total / (len(n_values) * 5)
    rho_non_ip2_avg = rho_non_ip2_total / (len(n_values) * 5)
    
    if rho_non_ip2_avg >= n / 2:
        return {
            "metric_name": "Free Entropy",
            "metric_value": rho_non_ip2_avg,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "Non-IP2 BP with rho ≥ n/2"
        }
    else:
        return {
            "metric_name": "Free Entropy",
            "metric_value": rho_ip2_avg,
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    rho_ip2_total = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    rho_non_ip2_total = sum(r["metric_value"] for r in results if not r["conjecture_holds"])
    support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={rho_ip2_total/len(results)} std=NA support_fraction={support_fraction}")
    elif rho_non_ip2_total > 0:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Non-IP2 BP with rho ≥ n/2' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
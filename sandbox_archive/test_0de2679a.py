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
    
    def sign_matrix(n):
        M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        return M
    
    def free_probability_entanglement_invariant(M):
        n = len(M)
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if M[i][j] != -M[j][i]:
                    count += 1
        return count / (n * (n-1) // 2)
    
    def disjointness_instance(n):
        A = [random.choice([0, 1]) for _ in range(n)]
        B = [random.choice([0, 1]) for _ in range(n)]
        return A, B
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_tau = 0
        
        for _ in range(5):  # Sample 5 instances per size
            M = sign_matrix(n)
            tau_M = free_probability_entanglement_invariant(M)
            total_tau += tau_M
            instances_tested += 1
        
        avg_tau = total_tau / instances_tested
        results.append({"n": n, "avg_tau": avg_tau})
    
    metric_value = sum(result["avg_tau"] for result in results) / len(results)
    conjecture_holds = all(result["avg_tau"] >= n for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Average Free Probability Entanglement Invariant",
        "metric_value": metric_value,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
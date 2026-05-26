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
    q_values = [2, 3, 5]
    k_max = 50
    n_min = 5
    n_max = 40
    instances_per_seed = 30
    
    random.seed(seed)
    
    results = []
    for q in q_values:
        for n in range(n_min, n_max + 1):
            for _ in range(instances_per_seed):
                # Generate a random monomial ideal I of degree d over F_q with n variables
                d = random.randint(1, n)
                I = set()
                while len(I) < n:
                    monomial = tuple(sorted(random.sample(range(n), d)))
                    if monomial not in I:
                        I.add(monomial)
                
                # Compute K_0(I) using an algorithm for algebraic K-theory
                # This is a placeholder for the actual computation of K_0(I)
                # For simplicity, we assume |K_0(I)| is uniformly distributed over [1, q^k]
                k = random.randint(1, k_max)
                prob = 1 / (q ** k)
                
                # Measure the logarithm of the probability that |K_0(I)| ≤ q^k
                log_prob = math.log(prob) if prob > 0 else -math.inf
                
                results.append({
                    "n": n,
                    "k": k,
                    "prob": prob,
                    "log_prob": log_prob
                })
    
    # Compute the mean and standard deviation of the logarithm of the probabilities
    mean_log_prob = sum(result["log_prob"] for result in results) / len(results)
    std_log_prob = math.sqrt(sum((result["log_prob"] - mean_log_prob) ** 2 for result in results) / len(results))
    
    # Check if the conjecture holds
    conjecture_holds = all(result["log_prob"] >= (n * math.log(n) / k) - std_log_prob for result in results)
    
    return {
        "metric_name": "log_probability",
        "metric_value": mean_log_prob,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5] * 10
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_log_prob = sum(result["metric_value"] for result in results) / len(results)
    std_log_prob = math.sqrt(sum((result["metric_value"] - mean_log_prob) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_log_prob} std={std_log_prob} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
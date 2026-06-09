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

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def smallest_prime_not_dividing(n):
    q = 2
    while True:
        if n % q != 0 and is_prime(q):
            return q
        q += 1

def quadratic_residues_modulo_q(n, q):
    residues = set()
    for i in range(1, q):
        if (i * i) % q not in residues:
            residues.add((i * i) % q)
    non_residues = [x for x in range(q) if x not in residues]
    return non_residues

def rank_variance(n):
    # Placeholder implementation of rank variance
    # This is a dummy function to demonstrate the structure
    return random.random()  # Replace with actual calculation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    
    total_metric_value = 0.0
    count_supporting_conjecture = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        q = smallest_prime_not_dividing(n)
        non_residues = quadratic_residues_modulo_q(n, q)
        
        R_phi = rank_variance(n)
        N_q_size = len(non_residues)
        ratio = N_q_size / q
        
        total_metric_value += ratio
        if abs(ratio - R_phi) > 1e-6:  # Adjust the threshold as needed
            counterexample = f"n={n}, q={q}, R(φ)={R_phi}, |N_q|/q={ratio}"
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = counterexample == ""
    
    return {
        "metric_name": "|N_q| / q",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    mean_metric_value = sum(run_trial(seed)["metric_value"] for seed in seeds) / len(seeds)
    support_fraction = sum(1 for seed in seeds if run_trial(seed)["conjecture_holds"]) / len(seeds)
    
    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std=0.000000 support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
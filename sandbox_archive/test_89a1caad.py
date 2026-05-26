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
    
    q_values = [2, 3, 5]
    k_max = 50
    n_min = 5
    n_max = 40
    instances_per_seed = 30
    
    results = []
    
    for _ in range(instances_per_seed):
        n = random.randint(n_min, n_max)
        d = random.randint(1, n)
        ideal = generate_random_monomial_ideal(n, d)
        
        for q in q_values:
            k_theory_group_order = compute_k_theory_group_order(ideal, q)
            if k_theory_group_order <= q**k_max:
                results.append(math.log(q**k_max / k_theory_group_order))
    
    if not results:
        return {
            "metric_name": "log_probability",
            "metric_value": 0.0,
            "instances_tested": instances_per_seed * len(q_values),
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    
    return {
        "metric_name": "log_probability",
        "metric_value": mean,
        "instances_tested": instances_per_seed * len(q_values),
        "conjecture_holds": all(x >= mean + std_dev for x in results),
        "counterexample": ""
    }

def generate_random_monomial_ideal(n, d):
    variables = list(range(1, n+1))
    monomials = []
    
    def generate_monomial(degree):
        if degree == 0:
            return [1]
        elif degree == 1:
            return random.sample(variables, 1)
        else:
            term = random.choice(variables)
            remaining_degree = degree - 1
            return [term] + generate_monomial(remaining_degree)
    
    for _ in range(d):
        monomials.append(generate_monomial(degree=random.randint(1, d)))
    
    ideal = set()
    for monomial in monomials:
        product = 1
        for var in monomial:
            product *= var
        ideal.add(product)
    
    return ideal

def compute_k_theory_group_order(ideal, q):
    # Placeholder function to simulate computing K-theory group order
    # This is a dummy implementation and should be replaced with actual computation
    return len(ideal)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5] * 10
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result["metric_value"])
    
    if len(results) == len(seeds):
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
        support_fraction = 1.0
    else:
        mean = None
        std_dev = None
        support_fraction = len(results) / len(seeds)
    
    if all(trial_result["conjecture_holds"] for trial_result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
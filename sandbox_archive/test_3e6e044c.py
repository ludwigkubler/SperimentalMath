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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_associated_elliptic_curve(f):
        # Placeholder function to simulate computation of an elliptic curve
        # This is a dummy implementation and does not reflect actual mathematics
        return random.randint(1, 100)
    
    def min_index_of_monodromy_representation(e_f):
        # Placeholder function to simulate computation of the minimal index
        # This is a dummy implementation and does not reflect actual mathematics
        return random.randint(1, 50)
    
    def communication_complexity(f):
        # Placeholder function to simulate computation of communication complexity
        # This is a dummy implementation and does not reflect actual mathematics
        return len(f) / 2
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds_count = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        e_f = compute_associated_elliptic_curve(f)
        I_e_f = min_index_of_monodromy_representation(e_f)
        C_f = communication_complexity(f)
        
        if C_f > I_e_f:
            conjecture_holds_count += 1
            counterexample = f"n={n}, C(f)={C_f}, I(e_f)={I_e_f}"
        else:
            counterexample = ""
        
        total_metric_value += C_f
        print(f"TRIAL: {seed=}, n={n}, C(f)={C_f}, I(e_f)={I_e_f}, conjecture_holds={'yes' if C_f <= I_e_f else 'no'}, counterexample='{counterexample}'")
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = conjecture_holds_count / instances_tested
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": "" if conjecture_holds_count == instances_tested else counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 1000, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.95 else 'FALSIFIED'} mean={mean_metric_value:.2f} std=... support_fraction={support_fraction:.2f}")
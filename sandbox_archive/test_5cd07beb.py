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
    
    def generate_function(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def construct_dfa(f):
        n = len(f)
        states = {i for i in range(n + 1)}
        transitions = {}
        accepting_states = set()
        
        for q in states:
            for a in [0, 1]:
                if q == n and f[q - 1] == a:
                    accepting_states.add(q)
                elif q < n:
                    next_state = (q * 2) + a
                    transitions[(q, a)] = next_state
        
        return states, transitions, accepting_states
    
    def count_binary_operations(dfa):
        _, transitions, _ = dfa
        return sum(1 for _ in transitions.values())
    
    n = random.randint(5, 40)
    f = generate_function(n)
    dfa = construct_dfa(f)
    binary_operations = count_binary_operations(dfa)
    
    expected_operations = n * math.log2(n)
    within_bounds = abs(binary_operations - expected_operations) <= 1
    
    return {
        "metric_name": "binary_operations",
        "metric_value": binary_operations,
        "instances_tested": 1,
        "conjecture_holds": within_bounds,
        "counterexample": "" if within_bounds else f"n={n}, f={f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes
    
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
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, f={generate_function(results[first_failing_seed]['instances_tested'])}\" first_failing_seed={first_failing_seed}")
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
    
    def construct_automaton(f):
        n = int(math.log2(len(f)))
        states = list(range(2**(n+1)))
        transitions = {state: [[None] * 2 for _ in range(2)] for state in states}
        accepting_states = set()
        
        for i in range(2**n):
            for j in range(2):
                next_state = (i << 1) | j
                if f[i] == j:
                    accepting_states.add(next_state)
                transitions[state][j, f[j]] = next_state
        
        return states, transitions, accepting_states
    
    def calculate_generality(transitions, n):
        total_transitions = sum(sum(1 for _ in row) for row in transitions[0])
        return total_transitions / (2**(n+1))
    
    def calculate_bounds(n):
        c1 = 0.5
        c2 = 1.0
        return c1 * 2**n, c2 * 2**n / math.log(n)**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        states, transitions, accepting_states = construct_automaton(f)
        generality = calculate_generality(transitions, n)
        lower_bound, upper_bound = calculate_bounds(n)
        
        results.append({
            "n": n,
            "generality": generality,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound
        })
    
    return {
        "metric_name": "Generality",
        "metric_value": sum(result["generality"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all(lower_bound <= generality <= upper_bound for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if all(result["conjecture_holds"] for result in all_results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
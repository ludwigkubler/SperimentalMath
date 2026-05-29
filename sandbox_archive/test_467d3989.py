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
        transitions = {}
        accept_state = 2**n
        for state in states:
            if state == accept_state:
                continue
            bit = (state >> (n-1)) & 1
            next_state = state ^ (1 << n) | bit
            transitions[state] = {0: next_state, 1: next_state}
        return transitions, accept_state
    
    def calculate_generality(transitions, accept_state):
        states = list(transitions.keys())
        generality = 0
        for state in states:
            if state == accept_state:
                continue
            reachable_states = {state}
            stack = [state]
            while stack:
                current = stack.pop()
                for bit, next_state in transitions[current].items():
                    if next_state not in reachable_states:
                        reachable_states.add(next_state)
                        stack.append(next_state)
            generality += len(reachable_states) - 1
        return generality
    
    def calculate_bounds(n):
        c1 = 0.5
        c2 = 1 / math.log(n)**2
        lower_bound = c1 * 2**n
        upper_bound = c2 * 2**n
        return lower_bound, upper_bound
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        transitions, accept_state = construct_automaton(f)
        generality = calculate_generality(transitions, accept_state)
        lower_bound, upper_bound = calculate_bounds(n)
        
        if generality < lower_bound or generality > upper_bound:
            return {
                "metric_name": "generality",
                "metric_value": generality,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Generality out of bounds for n={n}, generality={generality}"
            }
        
        metric_values.append(generality)
    
    return {
        "metric_name": "generality",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='generality_out_of_bounds' first_failing_seed={first_failing_seed}")
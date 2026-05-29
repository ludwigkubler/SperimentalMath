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
        states = list(range(2**n))
        transitions = {state: [[None] * 2 for _ in range(2)] for state in states}
        accepting_states = set()
        
        for i in range(2**n):
            for j in range(n):
                if f[i ^ (1 << j)] == f[i]:
                    next_state = i
                else:
                    next_state = i ^ (1 << j)
                transitions[state][i, f[j]] = next_state
        
        accepting_states.add(0)  # Example: only state 0 is accepting
        return states, transitions, accepting_states
    
    def calculate_generality(transitions):
        n = len(next(iter(transitions.keys())))
        total_transitions = sum(sum(len(v) for v in vs) for vs in transitions.values())
        return total_transitions / (n * n)
    
    def predict_bound(n):
        c1 = 0.5
        c2 = 1.0
        return c1 * 2**n, c2 * 2**n / math.log(n)**2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        states, transitions, accepting_states = construct_automaton(f)
        generality = calculate_generality(transitions)
        c1_bound, c2_bound = predict_bound(n)
        
        results.append({
            "n": n,
            "generality": generality,
            "c1_bound": c1_bound,
            "c2_bound": c2_bound
        })
    
    mean_generality = sum(res["generality"] for res in results) / len(results)
    mean_c1_bound = sum(res["c1_bound"] for res in results) / len(results)
    mean_c2_bound = sum(res["c2_bound"] for res in results) / len(results)
    
    if all(mean_generality >= c1_bound and mean_generality <= c2_bound for res in results):
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "Generality",
        "metric_value": mean_generality,
        "instances_tested": len(results),
        "n_max": max(res["n"] for res in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean generality {mean_generality} out of bounds [{mean_c1_bound}, {mean_c2_bound}]"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Generality out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data n_tested={len(results)}")
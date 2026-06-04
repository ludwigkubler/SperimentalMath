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
    
    def generate_automaton(n):
        # Generate a random automaton with n states and edges
        states = list(range(n))
        transitions = {state: {} for state in states}
        for state in states:
            next_state = random.choice(states)
            while next_state == state:
                next_state = random.choice(states)
            transitions[state][0] = next_state
        return transitions
    
    def compute_monotone_width(transitions):
        # Compute the monotone width of the automaton
        n = len(transitions)
        width = 1
        for i in range(n):
            visited = [False] * n
            stack = [(i, 0)]
            while stack:
                current_state, depth = stack.pop()
                if not visited[current_state]:
                    visited[current_state] = True
                    for symbol in transitions[current_state]:
                        next_state = transitions[current_state][symbol]
                        stack.append((next_state, depth + 1))
            width = max(width, depth)
        return width
    
    def compute_automorphism_group(transitions):
        # Compute the automorphism group of the automaton
        n = len(transitions)
        group = []
        for perm in itertools.permutations(range(n)):
            is_automorphism = True
            for state in range(n):
                for symbol in transitions[state]:
                    if perm[state] != perm[transitions[state][symbol]]:
                        is_automorphism = False
                        break
                if not is_automorphism:
                    break
            if is_automorphism:
                group.append(perm)
        return group
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ord_L = []
    w_L = []
    
    for n in n_values:
        transitions = generate_automaton(n)
        ord_L.append(len(compute_automorphism_group(transitions)))
        w_L.append(compute_monotone_width(transitions))
    
    if not ord_L or not w_L:
        return {
            "metric_name": "ord(L) / w_L",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = [ord_L[i] / w_L[i] for i in range(len(ord_L))]
    mean_ratio = sum(ratio) / len(ratio)
    std_ratio = math.sqrt(sum((r - mean_ratio) ** 2 for r in ratio) / len(ratio))
    
    return {
        "metric_name": "ord(L) / w_L",
        "metric_value": mean_ratio,
        "instances_tested": len(ord_L),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= mean_ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] > 2 for r in results) or any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
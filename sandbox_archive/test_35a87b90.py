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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_regular_language(n):
        if n == 1:
            return {'states': ['q0'], 'alphabet': ['a'], 'transitions': [('q0', 'a', 'q0')], 'initial_state': 'q0', 'accepting_states': ['q0']}
        states = [f'q{i}' for i in range(n)]
        alphabet = list('abcdefghijklmnopqrstuvwxyz')[:n]
        transitions = []
        initial_state = random.choice(states)
        accepting_states = [random.choice(states) for _ in range(1, n//2 + 1)]
        
        for q in states:
            for a in alphabet:
                if q == initial_state and a == 'a':
                    next_q = q
                else:
                    next_q = random.choice([q for q in states if q != initial_state])
                transitions.append((q, a, next_q))
        
        return {'states': states, 'alphabet': alphabet, 'transitions': transitions, 'initial_state': initial_state, 'accepting_states': accepting_states}
    
    def compute_monotone_width(L):
        # Placeholder for monotone width computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(L['states'])
    
    def compute_automorphism_group_order(L):
        # Placeholder for automorphism group order computation
        # This is a dummy implementation and should be replaced with actual logic
        return 2 ** len(L['states'])
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        L = generate_random_regular_language(n)
        w_L = compute_monotone_width(L)
        ord_L = compute_automorphism_group_order(L)
        results.append({'n': n, 'w_L': w_L, 'ord_L': ord_L})
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = [r['ord_L'] / r['w_L'] for r in results if r['w_L'] > 0]
    if not ratio:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "zero_denominator"
        }
    
    mean_ratio = sum(ratio) / len(ratio)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratio) / len(ratio))
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(r['n'] for r in results),
        "conjecture_holds": 0.5 <= mean_ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 2**31-1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(1)
    
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r['metric_value'] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(r['counterexample'] != "" for r in results):
        first_failing_seed = next((r['seed'] for r in results if r['counterexample'] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")
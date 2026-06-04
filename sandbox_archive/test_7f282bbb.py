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
        # Generate a random automaton with n states
        states = list(range(n))
        alphabet = ['a', 'b']
        transition_table = {q: {} for q in states}
        start_state = 0
        accepting_states = [n-1]
        
        for q in states:
            for a in alphabet:
                next_q = random.choice(states)
                while next_q == q:
                    next_q = random.choice(states)
                transition_table[q][a] = next_q
        
        return {
            'states': states,
            'alphabet': alphabet,
            'transition_table': transition_table,
            'start_state': start_state,
            'accepting_states': accepting_states
        }
    
    def compute_monotone_width(automaton):
        # Compute the monotone width of the automaton
        n = len(automaton['states'])
        width = 0
        
        for q in automaton['states']:
            if q in automaton['accepting_states']:
                continue
            
            reachable_states = {q}
            while True:
                new_reachable_states = set()
                for a in automaton['alphabet']:
                    next_q = automaton['transition_table'][q][a]
                    if next_q not in reachable_states:
                        new_reachable_states.add(next_q)
                if not new_reachable_states:
                    break
                reachable_states.update(new_reachable_states)
            
            width = max(width, len(reachable_states))
        
        return width
    
    def compute_automorphism_group(automaton):
        # Compute the automorphism group of the automaton
        states = automaton['states']
        n = len(states)
        automorphisms = []
        
        for perm in itertools.permutations(states):
            is_automorphism = True
            for q in states:
                for a in automaton['alphabet']:
                    next_q = automaton['transition_table'][q][a]
                    if automaton['transition_table'][perm[q]][a] != perm[next_q]:
                        is_automorphism = False
                        break
                if not is_automorphism:
                    break
            
            if is_automorphism:
                automorphisms.append(perm)
        
        return len(automorphisms)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ord_L_values = []
    w_L_values = []
    
    for n in n_values:
        automaton = generate_automaton(n)
        ord_L = compute_automorphism_group(automaton)
        w_L = compute_monotone_width(automaton)
        
        ord_L_values.append(ord_L)
        w_L_values.append(w_L)
    
    if not ord_L_values or not w_L_values:
        return {
            "metric_name": "ord(L) / w_L",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = sum(ord_L_values[i] / w_L_values[i] for i in range(len(n_values))) / len(n_values)
    if not (0.5 <= ratio <= 2):
        return {
            "metric_name": "ord(L) / w_L",
            "metric_value": ratio,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Ratio {ratio} outside [0.5, 2]"
        }
    
    return {
        "metric_name": "ord(L) / w_L",
        "metric_value": ratio,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result['conjecture_holds'] for result in results):
        mean_ratio = sum(result['metric_value'] for result in results) / len(results)
        std_dev = math.sqrt(sum((result['metric_value'] - mean_ratio) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result['conjecture_holds']]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(result['metric_value'] > 2 or result['metric_value'] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result['metric_value'] > 2 or result['metric_value'] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside [0.5, 2]\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")
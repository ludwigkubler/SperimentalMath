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
    
    def generate_automaton(n):
        if n == 1:
            return {'states': [0], 'alphabet': ['a'], 'transitions': {0: {'a': 0}}, 'initial_state': 0, 'accepting_states': [0]}
        states = list(range(n))
        alphabet = ['a', 'b']
        transitions = {}
        initial_state = random.choice(states)
        accepting_states = random.sample(states, random.randint(1, n))
        
        for state in states:
            transitions[state] = {symbol: random.choice(states) for symbol in alphabet}
        
        return {'states': states, 'alphabet': alphabet, 'transitions': transitions, 'initial_state': initial_state, 'accepting_states': accepting_states}
    
    def automaton_to_language(automaton):
        states = automaton['states']
        alphabet = automaton['alphabet']
        transitions = automaton['transitions']
        initial_state = automaton['initial_state']
        accepting_states = automaton['accepting_states']
        
        language = set()
        queue = [(initial_state, '')]
        
        while queue:
            current_state, prefix = queue.pop(0)
            if current_state in accepting_states:
                language.add(prefix)
            
            for symbol in alphabet:
                next_state = transitions[current_state][symbol]
                queue.append((next_state, prefix + symbol))
        
        return language
    
    def automorphism_group_size(automaton):
        states = automaton['states']
        transitions = automaton['transitions']
        n = len(states)
        
        group = []
        
        for perm in itertools.permutations(range(n)):
            valid = True
            for state in states:
                for symbol in automaton['alphabet']:
                    if perm[transitions[state][symbol]] != transitions[perm[state]][symbol]:
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                group.append(perm)
        
        return len(group)
    
    def monotone_width(language):
        n = len(language)
        width = 0
        
        for subset in itertools.chain.from_iterable(itertools.combinations(language, r) for r in range(n + 1)):
            subset_set = set(subset)
            if all(word.startswith(prefix) for word in language if word in subset_set):
                width = max(width, len(subset))
        
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        automaton = generate_automaton(n)
        language = automaton_to_language(automaton)
        ord_L = automorphism_group_size(automaton)
        w_L = monotone_width(language)
        
        if ord_L == 0 or w_L == 0:
            continue
        
        metric_values.append(ord_L / w_L)
    
    if not metric_values:
        return {
            "metric_name": "ord(L) / w_L",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_metric_values"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "ord(L) / w_L",
        "metric_value": mean,
        "instances_tested": len(metric_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= mean <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **{result}}}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r['conjecture_holds'])
    support_fraction = supported_count / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results))) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='ord(L) / w_L out of bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")
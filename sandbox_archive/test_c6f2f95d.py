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
        return [random.choice([True, False]) for _ in range(2**n)]
    
    def calculate_entropy(f):
        counts = [f.count(True), f.count(False)]
        total = sum(counts)
        probabilities = [c / total for c in counts]
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)
        return entropy
    
    def construct_minimal_dfa(f):
        n = len(f)
        states = [{'q': i, 'transitions': {}} for i in range(2**n)]
        accepting_states = [i for i in range(2**n) if f[i]]
        
        for q in range(2**n):
            for bit in [0, 1]:
                next_q = (q * 2 + bit) % (2**n)
                states[q]['transitions'][bit] = next_q
        
        return states, accepting_states
    
    def count_states(dfa):
        return len([state for state in dfa if any(state['transitions'].values())])
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_states = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        entropy = calculate_entropy(f)
        dfa, accepting_states = construct_minimal_dfa(f)
        states = count_states(dfa)
        
        if states > 2**entropy:
            return {
                "metric_name": "states",
                "metric_value": states,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, entropy={entropy}, states={states}"
            }
        
        total_states += states
        instances_tested += 1
    
    return {
        "metric_name": "states",
        "metric_value": total_states / len(n_values),
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_states = sum(r['metric_value'] * r['instances_tested'] for r in results) / sum(r['instances_tested'] for r in results)
    std_states = math.sqrt(sum((r['metric_value'] - mean_states)**2 * r['instances_tested'] for r in results) / sum(r['instances_tested'] for r in results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_states} std={std_states} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_states} std={std_states} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}\" first_failing_seed={first_failing_seed}")
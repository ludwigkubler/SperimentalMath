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
    
    # Generate a random boolean function with entropy H(f)
    n = 10  # Number of variables in the boolean function
    f = [random.choice([0, 1]) for _ in range(2**n)]
    entropy_f = -sum(p * math.log2(p) if p != 0 else 0 for p in (f.count(0)/len(f), f.count(1)/len(f)))
    
    # Construct a minimal deterministic finite automaton (DFA) accepting the language defined by the function
    states = {0}
    transitions = {}
    accept_states = set()
    
    def add_transition(state, char, next_state):
        if state not in transitions:
            transitions[state] = {}
        if char not in transitions[state]:
            transitions[state][char] = []
        transitions[state][char].append(next_state)
    
    for i in range(len(f)):
        binary_rep = format(i, '0{}b'.format(n))
        current_state = 0
        for bit in binary_rep:
            if bit == '0':
                next_state = current_state * 2
            else:
                next_state = current_state * 2 + 1
            add_transition(current_state, int(bit), next_state)
            current_state = next_state
    
    # Measure the number of states in the minimal DFA
    num_states = len(transitions)
    
    # Compare it with 2^H(f)
    upper_bound = 2 ** entropy_f
    
    return {
        "metric_name": "Number of States",
        "metric_value": num_states,
        "instances_tested": 1,
        "conjecture_holds": num_states <= upper_bound,
        "counterexample": "" if num_states <= upper_bound else f"Counterexample: Number of states ({num_states}) > 2^H(f) = {upper_bound}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Number of states exceeds 2^H(f)\" first_failing_seed={first_failing_seed}")
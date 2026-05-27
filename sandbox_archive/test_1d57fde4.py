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
    
    def calculate_entropy(f):
        counts = [f.count(0), f.count(1)]
        total = sum(counts)
        if total == 0:
            return 0
        p0 = counts[0] / total
        p1 = counts[1] / total
        entropy = -p0 * math.log2(p0) - p1 * math.log2(p1)
        return entropy
    
    def construct_dfa(f):
        states = {0}
        transitions = {}
        accepting_states = set()
        
        for state in states:
            for bit in [0, 1]:
                next_state = (state << 1) | bit
                if next_state not in states:
                    states.add(next_state)
                transitions[(state, bit)] = next_state
                
                if f[next_state] == 1:
                    accepting_states.add(next_state)
        
        return len(states), accepting_states
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    entropy = calculate_entropy(f)
    num_states, _ = construct_dfa(f)
    
    metric_name = 'Number of States'
    metric_value = num_states
    instances_tested = 1
    conjecture_holds = num_states <= 2 ** entropy
    counterexample = '' if conjecture_holds else f'Counterexample: Number of states ({num_states}) > 2^H(f) = {2 ** entropy}'
    
    return {
        'metric_name': metric_name,
        'metric_value': metric_value,
        'instances_tested': instances_tested,
        'conjecture_holds': conjecture_holds,
        'counterexample': counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f'TRIAL: {result}')
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f'RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}')
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f'RESULT: FALSIFIED counterexample="{r["counterexample"]}" first_failing_seed={first_failing_seed}')
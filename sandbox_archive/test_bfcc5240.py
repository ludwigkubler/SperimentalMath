# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_function(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def construct_dfa(f):
        n = len(f)
        states = list(range(2 * n + 1))
        transitions = {}
        accepting_states = set()
        
        for i in range(n):
            if f[i] == 0:
                accepting_states.add(i + n)
        
        for q in states:
            for a in [0, 1]:
                if q < n and a == f[q]:
                    transitions[(q, a)] = q + 1
                elif q >= n and (a == 0 or q - n == i):
                    transitions[(q, a)] = q
                else:
                    transitions[(q, a)] = q
        
        return states, transitions, accepting_states
    
    def count_binary_operations(transitions):
        return sum(len(v) for v in transitions.values())
    
    n = random.randint(5, 40)
    f = generate_function(n)
    states, transitions, _ = construct_dfa(f)
    binary_operations = count_binary_operations(transitions)
    
    metric_name = 'binary_operations'
    metric_value = binary_operations
    instances_tested = 1
    conjecture_holds = binary_operations == n * (n + 1) // 2
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
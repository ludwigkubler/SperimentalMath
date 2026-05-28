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
    
    def construct_dfa(f):
        n = len(f)
        states = set()
        transitions = {}
        
        for i in range(n):
            if f[i] == 0:
                states.add(i)
                for j in range(n):
                    if f[j] == i + 1:
                        if (i, j) not in transitions:
                            transitions[(i, j)] = []
                        transitions[(i, j)].append(j)
        
        return states, transitions
    
    def is_dfa_recognizing(f, dfa):
        states, transitions = dfa
        start_state = 0
        if start_state not in states:
            return False
        
        def dfs(state, visited):
            if state in visited:
                return True
            visited.add(state)
            for next_state in transitions.get((state, f[state]), []):
                if not dfs(next_state, visited):
                    return False
            visited.remove(state)
            return True
        
        return dfs(start_state, set())
    
    def count_binary_operations(dfa):
        states, transitions = dfa
        count = 0
        for state in states:
            for next_state in transitions.get((state, f[state]), []):
                count += 1
        return count
    
    n = random.randint(5, 40)
    f = [random.randint(0, n-1) for _ in range(n)]
    
    dfa = construct_dfa(f)
    if not dfa:
        return {
            "metric_name": "binary_operations",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    binary_operations = count_binary_operations(dfa)
    conjecture_holds = binary_operations == n * math.log2(n) and is_dfa_recognizing(f, dfa)
    
    return {
        "metric_name": "binary_operations",
        "metric_value": binary_operations,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)
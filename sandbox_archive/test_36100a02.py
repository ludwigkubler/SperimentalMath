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
    
    primes = [3, 5, 7, 11, 13, 17, 19, 23]
    depths = [2, 3, 4]
    constructions = ['flat', 'balanced', 'Håstad']
    
    results = []
    for n in primes:
        for d in depths:
            for construction in constructions:
                # Generate a random AC⁰ circuit
                if construction == 'flat':
                    s = 2**(n-1)
                elif construction == 'balanced':
                    s = 2**d * (n - 1) + n - 1
                elif construction == 'Håstad':
                    s = 2**(d+1) * (n - 1) + n - 1
                
                # Compute ψ(C)
                def hash_gate(g):
                    return (g['op'], tuple(sorted(hash(child) for child in g['children'])), sorted(g['inputs']))
                
                def apply_shifts(index_multiset, shift):
                    return sorted((i + shift) % n for i in index_multiset)
                
                gates = [{'op': 'AND', 'children': [], 'inputs': []}, {'op': 'OR', 'children': [], 'inputs': []}]
                for _ in range(s - 2):
                    gate_type = random.choice(['AND', 'OR'])
                    children = random.sample(gates, 2)
                    inputs = [len(g['inputs']) for g in children]
                    gates.append({'op': gate_type, 'children': children, 'inputs': inputs})
                
                canonical_forms = {}
                for i, g in enumerate(gates):
                    index_multiset = sorted(i for _ in range(len(g['inputs'])))
                    for shift in range(n):
                        shifted_index_multiset = apply_shifts(index_multiset, shift)
                        key = hash_gate({'op': 'shift', 'children': [], 'inputs': shifted_index_multiset})
                        if key not in canonical_forms:
                            canonical_forms[key] = []
                        canonical_forms[key].append(i)
                
                ψ_C = len(canonical_forms)
                
                # Compute the ratio
                r = 4 * d * ψ_C / math.log2(s)
                results.append((ψ_C, s, d, r))
    
    min_r = min(r for _, _, _, r in results)
    conjecture_holds = min_r >= 1.0
    
    return {
        "metric_name": "r",
        "metric_value": min_r,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"min r = {min_r} < 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
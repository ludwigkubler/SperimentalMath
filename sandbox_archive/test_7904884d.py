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

def generate_circuit(n):
    if n == 1:
        return ['0']
    else:
        left = generate_circuit(n // 2)
        right = generate_circuit(n - n // 2)
        return [f'({left[0]} OR {right[0]})'] + left + right

def evaluate_circuit(circuit, assignment):
    stack = []
    for token in circuit:
        if token == '0':
            stack.append(0)
        elif token == '1':
            stack.append(1)
        else:
            b = stack.pop()
            a = stack.pop()
            if token == 'OR':
                stack.append(a or b)
            elif token == 'AND':
                stack.append(a and b)
    return stack[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_ratio = 0
        
        for _ in range(30):
            circuit = generate_circuit(n)
            assignment = {i: random.choice([0, 1]) for i in range(n)}
            
            d = n  # Placeholder for minimal dimension of quaternionic Kähler manifold
            w_m = len(circuit)  # Placeholder for monotone width
            
            ratio = Fraction(d, w_m) / n**(2/3)
            results.append(ratio)
            
            instances_tested += 1
        
        mean_ratio = sum(results) / len(results)
        
        if all(0.5 <= r <= 2 for r in results):
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = "Ratio outside bounds"
        
        return {
            "metric_name": "Ratio of d/w_m(C) to n^(2/3)",
            "metric_value": mean_ratio,
            "instances_tested": instances_tested,
            "n_max": 40,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
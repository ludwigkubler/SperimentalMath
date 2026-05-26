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
    
    def generate_circuit(w, d):
        if w == 1 and d == 1:
            return ['x1']
        elif w == 1:
            return [f'~x{i}' for i in range(2, d+2)]
        else:
            left = generate_circuit(w//2, d-1)
            right = generate_circuit(w-w//2, d-1)
            return ['&', '(' + ' | '.join(left) + ')', '(' + ' & '.join(right) + ')']
    
    def evaluate_circuit(circuit):
        stack = []
        operators = {'&': lambda a, b: a and b, '|': lambda a, b: a or b}
        
        for token in circuit:
            if isinstance(token, list):
                operator = operators[token[0]]
                b = stack.pop()
                a = stack.pop()
                result = operator(a, b)
                stack.append(result)
            else:
                stack.append(True if token == 'x1' else False)
        
        return stack.pop()
    
    def frege_proof_width(formula):
        if isinstance(formula, list):
            return max(frege_proof_width(subformula) for subformula in formula[1:])
        else:
            return 1
    
    width = random.randint(5, 40)
    depth = random.randint(5, 40)
    circuit = generate_circuit(width, depth)
    
    result = evaluate_circuit(circuit)
    if result is None or not isinstance(result, bool):
        return {
            "metric_name": "frege_proof_width",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    frege_width = frege_proof_width(circuit)
    expected_min_rank = 2**(width/2 + depth)
    
    return {
        "metric_name": "frege_proof_width",
        "metric_value": frege_width,
        "instances_tested": 1,
        "conjecture_holds": frege_width >= expected_min_rank,
        "counterexample": "" if frege_width >= expected_min_rank else f"Expected min rank {expected_min_rank}, got {frege_width}"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
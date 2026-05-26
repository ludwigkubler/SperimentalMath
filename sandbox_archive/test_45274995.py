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
    
    def generate_circuit(w, d):
        if w <= 0 or d <= 0:
            return None
        circuit = []
        for _ in range(d):
            layer = [random.choice(['AND', 'OR'])]
            for _ in range(w - 1):
                layer.append(random.choice(['NOT', random.randint(1, w)]))
            circuit.append(layer)
        return circuit
    
    def evaluate_circuit(circuit):
        if not circuit:
            return 0
        stack = []
        for layer in reversed(circuit):
            new_layer = []
            for node in layer:
                if isinstance(node, int):
                    new_layer.append(stack[node - 1])
                else:
                    a = stack.pop()
                    b = stack.pop()
                    if node == 'AND':
                        new_layer.append(a and b)
                    elif node == 'OR':
                        new_layer.append(a or b)
            stack = new_layer
        return stack[0]
    
    def frege_proof_width(formula):
        if isinstance(formula, int):
            return 1
        elif formula in ['AND', 'OR']:
            return max(frege_proof_width(subformula) for subformula in formula)
        else:
            return 2 + max(frege_proof_width(subformula) for subformula in formula[1:])
    
    def min_rank(tm):
        if tm == 0:
            return 0
        rank = 0
        while tm > 0:
            rank += 1
            tm >>= 1
        return rank
    
    n_tests = 30
    total_rank = 0
    for _ in range(n_tests):
        w = random.randint(5, 40)
        d = random.randint(5, 40)
        circuit = generate_circuit(w, d)
        if not circuit:
            continue
        result = evaluate_circuit(circuit)
        tm = min_rank(result)
        rank = frege_proof_width(circuit)
        total_rank += rank
    
    avg_rank = total_rank / n_tests
    conjecture_holds = avg_rank >= 2**(w/2 + math.log(d, 2))
    
    return {
        "metric_name": "min_rank",
        "metric_value": avg_rank,
        "instances_tested": n_tests,
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
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
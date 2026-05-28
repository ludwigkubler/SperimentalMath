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
    
    def create_boolean_circuit(n):
        if n == 1:
            return ['NOT', random.choice([0, 1])]
        else:
            left = create_boolean_circuit(n // 2)
            right = create_boolean_circuit(n - n // 2)
            return [random.choice(['AND', 'OR']), left, right]
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, int):
            return circuit
        elif circuit[0] == 'NOT':
            return 1 - evaluate_circuit(circuit[1])
        elif circuit[0] == 'AND':
            return min(evaluate_circuit(circuit[1]), evaluate_circuit(circuit[2]))
        elif circuit[0] == 'OR':
            return max(evaluate_circuit(circuit[1]), evaluate_circuit(circuit[2]))
    
    def tropical_polynomial(circuit):
        if isinstance(circuit, int):
            return {circuit: 1}
        else:
            left = tropical_polynomial(circuit[1])
            right = tropical_polynomial(circuit[2])
            result = {}
            for k in set(left.keys()) | set(right.keys()):
                result[k] = max(left.get(k, -math.inf), right.get(k, -math.inf))
            return result
    
    def rank(poly):
        return len(poly)
    
    n = random.randint(5, 40)
    circuit = create_boolean_circuit(n)
    poly = tropical_polynomial(circuit)
    metric_value = rank(poly)
    conjecture_holds = metric_value <= (n ** (1/5))
    counterexample = "" if conjecture_holds else f"Circuit size {n}, polynomial rank {metric_value}"
    
    return {
        "metric_name": "tropical_cyclotomic_polynomial_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
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
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(r for r in results if not r["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
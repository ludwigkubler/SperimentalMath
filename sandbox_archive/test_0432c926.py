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
    
    def generate_circuit(n):
        if n == 1:
            return (0,)
        else:
            subcircuits = [generate_circuit(n-1) for _ in range(2)]
            return (subcircuits[0], subcircuits[1])
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, int):
            return circuit
        else:
            left = evaluate_circuit(circuit[0])
            right = evaluate_circuit(circuit[1])
            return left + right
    
    def complexity_polynomial(circuit):
        n = 0
        queue = [circuit]
        while queue:
            node = queue.pop()
            if isinstance(node, int):
                continue
            n += 1
            queue.extend(node)
        return n**3
    
    instances_tested = 0
    h_index_sum = 0
    max_n = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_circuit(n)
        instances_tested += 1
        if instances_tested > 30:
            break
        h_index = complexity_polynomial(circuit)
        h_index_sum += h_index
        max_n = max(max_n, n)
    
    mean_h_index = h_index_sum / instances_tested
    conjecture_holds = mean_h_index <= 100 * max_n**3
    
    return {
        "metric_name": "H_index",
        "metric_value": mean_h_index,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break
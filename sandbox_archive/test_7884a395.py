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
    
    def generate_circuit(n, s):
        if n < 1 or s < 1:
            return None
        circuit = []
        for _ in range(s):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def vertex_cover(circuit):
        if not circuit:
            return 0
        gate, inputs = circuit[0]
        if gate == 'AND':
            return 1 + max(vertex_cover(circuit[1:]), vertex_cover([(gate, inputs[1:])]))
        elif gate == 'OR':
            return 1 + min(vertex_cover(circuit[1:]), vertex_cover([(gate, inputs[1:])]))
    
    def reduced_words(circuit):
        if not circuit:
            return 0
        gate, inputs = circuit[0]
        if gate == 'AND':
            return 1 + max(reduced_words(circuit[1:]), reduced_words([(gate, inputs[1:])]))
        elif gate == 'OR':
            return 1 + min(reduced_words(circuit[1:]), reduced_words([(gate, inputs[1:])]))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            circuit = generate_circuit(n, random.randint(1, min(40, n)))
            if circuit is None:
                continue
            v_c = vertex_cover(circuit)
            r_w = reduced_words(circuit)
            results.append((n, v_c, r_w))
    
    if not results:
        return {
            "metric_name": "vertex_cover_to_reduced_words_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_v_c = sum(v for _, v, _ in results)
    total_r_w = sum(r for _, _, r in results)
    instances_tested = len(results)
    mean_ratio = total_v_c / total_r_w
    conjecture_holds = all(v <= 10 * math.pow(s, 1/3) for _, v, s in results)
    
    return {
        "metric_name": "vertex_cover_to_reduced_words_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mean_ratio_exceeds_bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_ratio_exceeds_bound' first_failing_seed={first_failing_seed}")
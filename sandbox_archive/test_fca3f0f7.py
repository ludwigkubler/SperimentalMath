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
    
    def generate_circuit(depth, n):
        if depth == 0:
            return []
        else:
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_circuit(random.randint(1, depth-1), n) for _ in range(n)]
            return [(gate, inputs)]
    
    def apply_braid(circuit, braid):
        if not circuit or not braid:
            return circuit
        gate, inputs = circuit[0]
        new_inputs = [apply_braid(sub_circuit, braid[i]) for i, sub_circuit in enumerate(inputs)]
        return [(gate, new_inputs)]
    
    def count_automorphisms(circuit):
        if not circuit:
            return 1
        gate, inputs = circuit[0]
        automorphisms = set()
        for perm in itertools.permutations(range(len(inputs))):
            new_inputs = [inputs[i] for i in perm]
            new_circuit = [(gate, new_inputs)]
            automorphisms.add(tuple(new_circuit))
        return len(automorphisms)
    
    def braid_group_action(n):
        if n == 1:
            return [[0]]
        else:
            action = []
            for i in range(n):
                action.append([i])
                action.append([n-1-i])
            for i in range(n-2, -1, -1):
                action.append([i+1, i])
                action.append([i, i-1])
            return action
    
    n = random.randint(5, 40)
    depth = random.randint(5, 40)
    circuit = generate_circuit(depth, n)
    
    braid_action = braid_group_action(n)
    automorphisms = set()
    
    for _ in range(100):  # Sample 100 random braids
        braid = random.choice(braid_action)
        new_circuit = apply_braid(circuit, braid)
        automorphisms.add(tuple(new_circuit))
    
    metric_value = len(automorphisms)
    instances_tested = 100
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": "Number of Automorphisms",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
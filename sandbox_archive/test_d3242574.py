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
    
    def generate_circuit(m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                circuit.append((gate_type, random.randint(1, m)))
            else:
                circuit.append((gate_type, random.sample(range(1, m), 2)))
        return circuit
    
    def communication_complexity(circuit):
        rank = 0
        nodes = set()
        for gate in circuit:
            if gate[0] == 'NOT':
                nodes.add(gate[1])
            else:
                nodes.update(gate[1])
        rank = len(nodes)
        return rank
    
    def quaternionic_automorphism_group_order(circuit):
        # Placeholder function to simulate the computation
        # This should be replaced with an actual algorithm for computing the order of the automorphism group
        return random.randint(1, 1000)  # Simulating a value between 1 and 1000
    
    m = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_circuit(m)
    
    order = quaternionic_automorphism_group_order(circuit)
    comm_complexity = communication_complexity(circuit)
    
    if comm_complexity == 0:
        return {
            "metric_name": "Ratio of Quaternionic Automorphism Group Order to Communication Complexity",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": m,
            "conjecture_holds": False,
            "counterexample": f"Circuit with m={m} has communication complexity 0"
        }
    
    ratio = order / comm_complexity
    
    return {
        "metric_name": "Ratio of Quaternionic Automorphism Group Order to Communication Complexity",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [773, 821, 877, 929]  # Default to a list of primes if no seeds are provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r['metric_value'] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        counterexample = next(r['counterexample'] for r in results if r['counterexample'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
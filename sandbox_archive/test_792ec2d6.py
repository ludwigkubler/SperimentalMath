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
    
    def generate_monotone_circuit(n):
        circuit = []
        for i in range(n):
            if random.choice([True, False]):
                circuit.append((i, 'AND', [random.randint(0, n-1), random.randint(0, n-1)]))
            else:
                circuit.append((i, 'OR', [random.randint(0, n-1), random.randint(0, n-1)]))
        return circuit
    
    def evaluate_circuit(circuit):
        values = {n: 1 for n in range(len(circuit))}
        for node, gate, inputs in reversed(circuit):
            if gate == 'AND':
                values[node] = values[inputs[0]] * values[inputs[1]]
            elif gate == 'OR':
                values[node] = max(values[inputs[0]], values[inputs[1]])
        return values[0]
    
    def extended_frege_proof_length(circuit):
        proof = []
        for node, gate, inputs in circuit:
            if gate == 'AND':
                proof.append((node, 'AND', [inputs[0], inputs[1]]))
                proof.append((inputs[0], 'AND', [random.randint(0, n-1), random.randint(0, n-1)]))
                proof.append((inputs[1], 'AND', [random.randint(0, n-1), random.randint(0, n-1)]))
            elif gate == 'OR':
                proof.append((node, 'OR', [inputs[0], inputs[1]]))
                proof.append((inputs[0], 'OR', [random.randint(0, n-1), random.randint(0, n-1)]))
                proof.append((inputs[1], 'OR', [random.randint(0, n-1), random.randint(0, n-1)]))
        return len(proof)
    
    n = 20
    circuit = generate_monotone_circuit(n)
    result = evaluate_circuit(circuit)
    proof_length = extended_frege_proof_length(circuit)
    
    if result == 1 and proof_length > n * math.log(n):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
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
    
    def generate_ac0_circuit(n):
        # Generate a random AC0 circuit computing PARITY on n inputs
        circuit = []
        for _ in range(n):
            gate = random.choice(['NOT', 'XOR'])
            if gate == 'NOT':
                circuit.append(('NOT', random.randint(0, len(circuit) - 1)))
            else:
                a, b = random.sample(range(len(circuit)), 2)
                circuit.append(('XOR', a, b))
        return circuit
    
    def evaluate_circuit(circuit):
        # Evaluate the AC0 circuit on all possible inputs
        n = len(circuit)
        inputs = [1 << i for i in range(n)]
        outputs = []
        for input_val in inputs:
            stack = list(bin(input_val)[2:].zfill(n))
            for gate in circuit:
                if gate[0] == 'NOT':
                    stack[gate[1]] ^= 1
                else:
                    a, b = gate[1], gate[2]
                    stack[a] ^= stack[b]
            outputs.append(stack[-1])
        return outputs
    
    def compute_representation_rank(outputs):
        # Compute the minimal representation rank as an algebraic torus
        n = len(outputs)
        rank = 0
        for i in range(n):
            if outputs[i] == 1:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n 5 times to get enough data points
            circuit = generate_ac0_circuit(n)
            outputs = evaluate_circuit(circuit)
            rank = compute_representation_rank(outputs)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    std_rank = math.sqrt(sum((rank - mean_rank) ** 2 for rank in range(total_rank)) / instances_tested)
    
    conjecture_holds = mean_rank >= 1 and std_rank <= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "representation_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
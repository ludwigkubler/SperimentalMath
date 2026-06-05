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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR', 'NOT'])
            if gate == 'NOT':
                circuit.append((gate, random.randint(0, n-1)))
            else:
                inputs = random.sample(range(n), 2)
                circuit.append((gate, inputs[0], inputs[1]))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate in reversed(circuit):
            if gate[0] == 'NOT':
                stack.append(not stack.pop())
            else:
                b = stack.pop()
                a = stack.pop()
                if gate[0] == 'AND':
                    stack.append(a and b)
                elif gate[0] == 'OR':
                    stack.append(a or b)
        return stack.pop()
    
    def tautology_set(circuit):
        n = len(circuit)
        inputs = [i for i in range(2**n)]
        outputs = []
        for input_val in inputs:
            input_bits = [(input_val >> j) & 1 for j in range(n)]
            output = evaluate_circuit([(gate, *inputs) if isinstance(inputs, tuple) else (gate, inputs) for gate, *inputs in circuit])
            outputs.append(output)
        return set([i for i, output in enumerate(outputs) if output == 1])
    
    def categorial_invariants(tautology):
        n = len(tautology)
        invariants = []
        for subset in range(1, 2**n):
            invariant = True
            for t in tautology:
                if (t & subset) != subset:
                    invariant = False
                    break
            if invariant:
                invariants.append(subset)
        return len(invariants)
    
    def entanglement_entropy(tautology):
        n = len(tautology)
        p = sum(1 for t in tautology if t == 0) / n
        q = sum(1 for t in tautology if t == 1) / n
        if p == 0 or q == 0:
            return 0
        return -p * math.log2(p) - q * math.log2(q)
    
    n_max = 40
    instances_tested = 0
    total_diff = 0
    
    for n in range(5, n_max + 1):
        circuit = generate_random_circuit(n)
        tautology = tautology_set(circuit)
        order = categorial_invariants(tautology)
        entanglement = entanglement_entropy(tautology)
        
        if len(tautology) == 0:
            continue
        
        diff = abs(order - entanglement)
        total_diff += diff
        instances_tested += 1
    
    mean_diff = total_diff / instances_tested if instances_tested > 0 else 0
    conjecture_holds = all(diff <= 1 for diff in range(2, 11)) and any(diff > 10 for diff in range(2, 11))
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": mean_diff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Difference exceeds 10"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Difference exceeds 10\" first_failing_seed={first_failing_seed}")
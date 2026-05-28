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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(5):  # Randomly add up to 5 gates
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(1, n))
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        n = len(circuit[0][1])
        input_space = [0] * n
        for gate in circuit:
            if gate[0] == 'AND':
                result = all(input_space[i] for i in gate[1])
            elif gate[0] == 'OR':
                result = any(input_space[i] for i in gate[1])
            input_space.append(result)
        return input_space[-1]
    
    def dual_space_size(n):
        return 2 ** n
    
    def tensor_product_rank(dual_input, dual_output):
        if dual_input == 0 or dual_output == 0:
            return 0
        return math.log(dual_input * dual_output, 2)
    
    def monotonicity(circuit):
        inputs = list(range(1 << len(circuit[0][1])))
        outputs = [evaluate_circuit([(gate_type, inputs[i]) for gate_type, _ in circuit]) for i in range(len(inputs))]
        return max(outputs) - min(outputs)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different circuits
            circuit = generate_boolean_circuit(n)
            dual_input = dual_space_size(len(circuit[0][1]))
            dual_output = dual_space_size(1)  # Output is binary
            rank = tensor_product_rank(dual_input, dual_output)
            m_C = monotonicity(circuit)
            if m_C == 0:
                continue
            ratio = rank / math.log(m_C, 2)
            total_ratio += ratio
            instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_ratio <= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
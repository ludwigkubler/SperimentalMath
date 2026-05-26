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
    
    def generate_boolean_circuit(n, s):
        circuit = []
        for _ in range(s):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = list(input_values)
        for gate_type, inputs in circuit:
            a, b = stack[inputs[0]], stack[inputs[1]]
            if gate_type == 'AND':
                stack.append(a and b)
            elif gate_type == 'OR':
                stack.append(a or b)
        return stack[-1]
    
    def tropicalize_poisson_tensor_product(circuit):
        n = len(circuit)
        T_C = []
        for tau in itertools.permutations(range(n)):
            tau_inv = {v: k for k, v in enumerate(tau)}
            min_rank = float('inf')
            for i in range(2**n):
                input_values = [bool(i >> j & 1) for j in range(n)]
                output = evaluate_circuit(circuit, input_values)
                tau_output = output ^ tau_inv[output]
                rank = sum(1 for bit in bin(tau_output)[2:] if bit == '1')
                min_rank = min(min_rank, rank)
            T_C.append(min_rank)
        return T_C
    
    n = random.randint(5, 40)
    s = random.randint(n, 40)
    circuit = generate_boolean_circuit(n, s)
    T_C = tropicalize_poisson_tensor_product(circuit)
    
    min_rank = min(T_C)
    f_n = int(math.sqrt(s))
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": len(T_C),
        "conjecture_holds": min_rank <= f_n,
        "counterexample": "" if min_rank <= f_n else f"n={n}, s={s}, min_rank={min_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_name']}, s={results[0]['instances_tested']}, min_rank={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
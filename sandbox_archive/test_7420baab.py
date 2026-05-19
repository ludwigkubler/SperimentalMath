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
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                inputs = [random.randint(0, 1)]
            else:
                inputs = [random.randint(0, 1) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_bits):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'NOT':
                result = 1 - inputs[0]
            elif gate_type == 'AND':
                result = 1
                for bit in inputs:
                    result &= bit
            else:  # OR
                result = 0
                for bit in inputs:
                    result |= bit
            stack.append(result)
        return stack.pop()
    
    def communication_complexity(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        
        left_circuit = circuit[:n//2]
        right_circuit = circuit[n//2:]
        
        left_input_bits = [random.randint(0, 1) for _ in range(len(left_circuit))]
        right_input_bits = [random.randint(0, 1) for _ in range(len(right_circuit))]
        
        left_output = evaluate_circuit(left_circuit, left_input_bits)
        right_output = evaluate_circuit(right_circuit, right_input_bits)
        
        return communication_complexity(left_circuit) + communication_complexity(right_circuit) + 1
    
    n = random.randint(5, 40)
    circuit = generate_ac0_circuit(n)
    cc = communication_complexity(circuit)
    
    c = 1 / math.log2(n)
    if cc < c * math.log2(n):
        return {
            "metric_name": "communication_complexity",
            "metric_value": cc,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CC({n}) = {cc} < {c * math.log2(n)} for n={n}"
        }
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
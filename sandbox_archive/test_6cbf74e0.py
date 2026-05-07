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
    
    def mod2(x):
        return x % 2
    
    def mod3(x):
        return x % 3
    
    def and_gate(a, b):
        return a and b
    
    def or_gate(a, b):
        return a or b
    
    def count_3AP(A_f, n):
        count = 0
        for x in range(2**n):
            for z in range(2**n):
                if (x + z) % 2 == 0:
                    y = (x + z) // 2
                    if y in A_f:
                        count += 1
        return count
    
    def generate_truth_table(depth, size, n):
        gates = []
        for _ in range(size):
            gate_type = random.choice(['and', 'or'])
            if gate_type == 'and':
                inputs = [random.choice([mod2, mod3]) for _ in range(2)]
            else:
                inputs = [random.choice([mod2, mod3]) for _ in range(2)]
            gates.append((gate_type, inputs))
        return gates
    
    def evaluate_circuit(circuit, n):
        truth_table = {}
        for i in range(2**n):
            input_bits = [(i >> j) & 1 for j in range(n)]
            output = input_bits[0]
            for gate_type, inputs in circuit:
                if gate_type == 'and':
                    output = and_gate(output, inputs[0](input_bits[inputs[1]]))
                else:
                    output = or_gate(output, inputs[0](input_bits[inputs[1]]))
            truth_table[i] = output
        return truth_table
    
    def R3(truth_table, n):
        A_f = set(key for key, value in truth_table.items() if value == 1)
        count = count_3AP(A_f, n)
        max_count = len(A_f)**3
        return count * 2**n / max(max_count, 1)
    
    def Sipser_function(n):
        fan_in = math.ceil(n**(1/3))
        truth_table = {}
        for i in range(2**n):
            input_bits = [(i >> j) & 1 for j in range(n)]
            output = input_bits[0]
            for j in range(fan_in - 1):
                if input_bits[j] == 1:
                    output = or_gate(output, input_bits[j + 1])
                else:
                    output = and_gate(output, input_bits[j + 1])
            truth_table[i] = output
        return truth_table
    
    n_values = [10, 12, 14]
    results = []
    
    for n in n_values:
        for _ in range(30):
            circuit = generate_truth_table(3, n**2, n)
            truth_table = evaluate_circuit(circuit, n)
            R3_value = R3(truth_table, n)
            results.append(R3_value)
    
    Sipser_R3 = R3(Sipser_function(14), 14)  # Using n=14 for consistency
    
    min_ACC0_R3 = min(results)
    conjecture_holds = min_ACC0_R3 >= 0.8 and Sipser_R3 <= 0.6
    counterexample = "" if conjecture_holds else "min ACC0 R3 < 0.8 or Sipser R3 > 0.6"
    
    return {
        "metric_name": "R3",
        "metric_value": min_ACC0_R3,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_R3 = sum(result["metric_value"] for result in results) / len(results)
    std_R3 = math.sqrt(sum((result["metric_value"] - mean_R3)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_R3} std={std_R3} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min ACC0 R3 < 0.8 or Sipser R3 > 0.6\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
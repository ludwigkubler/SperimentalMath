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
        for _ in range(random.randint(1, 5)):
            gate = random.choice(['AND', 'OR', 'NOT'])
            if gate == 'NOT':
                qubit = random.randint(0, n-1)
                circuit.append((gate, qubit))
            else:
                qubits = sorted(random.sample(range(n), 2))
                circuit.append((gate, qubits[0], qubits[1]))
        return circuit
    
    def depth_of_circuit(circuit):
        if not circuit:
            return 0
        max_depth = 0
        for gate in circuit:
            if gate[0] == 'NOT':
                max_depth = max(max_depth, depth_of_circuit([gate[1]]))
            else:
                max_depth = max(max_depth, depth_of_circuit([gate[2], gate[3]]))
        return 1 + max_depth
    
    def minimal_local_coherence(circuit):
        n = len(circuit)
        mlc = [0] * n
        for i in range(n):
            if circuit[i][0] == 'NOT':
                mlc[circuit[i][1]] += 1
            else:
                qubits = sorted([circuit[i][2], circuit[i][3]])
                mlc[qubits[0]] += 1
                mlc[qubits[1]] += 1
        return sum(mlc) / n
    
    instances_tested = 0
    total_mlc = 0
    total_depth = 0
    max_n = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_random_circuit(n)
        mlc = minimal_local_coherence(circuit)
        depth = depth_of_circuit(circuit)
        
        instances_tested += 1
        total_mlc += mlc
        total_depth += depth
        max_n = max(max_n, n)
    
    mean_mlc = total_mlc / instances_tested
    mean_depth = total_depth / instances_tested
    
    correlation_coefficient = (instances_tested * sum(mlc * depth for mlc, depth in zip(total_mlc, total_depth)) -
                                total_mlc * total_depth) / math.sqrt(
        instances_tested * sum(mlc**2 for mlc in total_mlc) - total_mlc**2 *
        instances_tested * sum(depth**2 for depth in total_depth) - total_depth**2)
    
    conjecture_holds = 0.8 <= correlation_coefficient <= 1.2
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_mlc = sum(r["metric_value"] for r in results) / len(results)
    std_mlc = math.sqrt(sum((r["metric_value"] - mean_mlc)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if 0.8 <= r["metric_value"] <= 1.2) / len(results)
    
    if all(0.8 <= r["metric_value"] <= 1.2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mlc} std={std_mlc} support_fraction={support_fraction}")
    elif any(not (0.8 <= r["metric_value"] <= 1.2) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.8 <= result["metric_value"] <= 1.2))
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
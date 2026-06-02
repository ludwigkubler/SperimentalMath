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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_weight(circuit):
        weight = 0
        for gate, inputs in circuit:
            if gate == 'AND':
                weight += sum(inputs)
            elif gate == 'OR':
                weight += max(inputs)
        return weight
    
    def frobenius_schur_indicators(circuit):
        indicators = []
        for _ in range(10):  # Sample 10 times to get a distribution
            state = [random.randint(0, 1) for _ in range(len(circuit))]
            indicator = 0
            for gate, inputs in circuit:
                if gate == 'AND':
                    indicator += sum(state[i] * inputs[i] for i in range(len(inputs)))
                elif gate == 'OR':
                    indicator += max(state[i] * inputs[i] for i in range(len(inputs)))
            indicators.append(indicator)
        return min(indicators)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_weight = 0
    min_order_FSInd = 0
    
    for n in n_values:
        circuit = generate_circuit(n)
        weight = compute_weight(circuit)
        order_FSInd = frobenius_schur_indicators(circuit)
        
        total_weight += weight
        min_order_FSInd += order_FSInd
    
    avg_weight = total_weight / len(n_values)
    avg_min_order_FSInd = min_order_FSInd / len(n_values)
    
    correlation_coefficient = (len(n_values) * sum(w * o for w, o in zip(n_values, n_values)) - 
                               sum(n_values) * sum(n_values)) / math.sqrt(
                                   (len(n_values) * sum(w**2 for w in n_values) - sum(n_values)**2) *
                                   (len(n_values) * sum(o**2 for o in n_values) - sum(n_values)**2))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
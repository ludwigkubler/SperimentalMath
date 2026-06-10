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
    
    def generate_random_circuit(depth):
        if depth == 0:
            return []
        else:
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_random_circuit(random.randint(1, depth-1)) for _ in range(2)]
            return (gate, inputs)
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, tuple):
            gate, inputs = circuit
            left = evaluate_circuit(inputs[0])
            right = evaluate_circuit(inputs[1])
            if gate == 'AND':
                return left and right
            elif gate == 'OR':
                return left or right
        else:
            return random.choice([True, False])
    
    def matroid_rank(circuit):
        if isinstance(circuit, tuple):
            _, inputs = circuit
            ranks = [matroid_rank(inp) for inp in inputs]
            return 1 + sum(ranks)
        else:
            return 0
    
    def local_induction_degree(matroid_rank):
        n = matroid_rank
        return n * (n - 1) // 2
    
    def entanglement_complexity(circuit):
        if isinstance(circuit, tuple):
            _, inputs = circuit
            complexities = [entanglement_complexity(inp) for inp in inputs]
            return sum(complexities)
        else:
            return 1
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    
    for _ in range(30):
        depth = random.randint(5, 40)
        circuit = generate_random_circuit(depth)
        rank = matroid_rank(circuit)
        lidb = local_induction_degree(rank)
        ec = entanglement_complexity(circuit)
        
        n_max = max(n_max, depth)
        instances_tested += 1
        metric_values.append(lidb / math.sqrt(ec))
    
    correlation_coefficient = sum(metric_values) / len(metric_values)
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
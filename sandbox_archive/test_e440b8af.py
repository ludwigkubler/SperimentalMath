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
    
    def generate_circuit(n, d):
        if d == 0:
            return [random.choice([0, 1])]
        else:
            inputs = [generate_circuit(1, d-1) for _ in range(n)]
            return [any(inputs), all(inputs)]
    
    def evaluate_circuit(circuit, input_values):
        while isinstance(circuit[0], list):
            circuit = circuit[0] if input_values.pop() else circuit[1]
        return circuit
    
    def hausdorff_dimension(output_set):
        # Simplified approximation of Hausdorff dimension for demonstration
        return len(output_set) ** (1 / math.log(len(output_set), 2))
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # 5 instances per size for statistical signal
            circuit = generate_circuit(n, random.randint(1, 10))
            input_values = [random.choice([0, 1]) for _ in range(n)]
            output = evaluate_circuit(circuit, input_values)
            if output:
                output_set = {tuple(input_values)}
                instances_tested += 1
                n_max = max(n_max, n)
                metric_values.append(hausdorff_dimension(output_set))
    
    correlation_coefficient = sum((x - (sum(metric_values) / len(metric_values))) * 
                                  (y - (n ** (-1/10))) for x, y in zip(metric_values, [n ** (-1/10)] * len(metric_values))) / \
                              math.sqrt(sum((x - (sum(metric_values) / len(metric_values))) ** 2 for x in metric_values)) / \
                              math.sqrt(sum((y - (n ** (-1/10))) ** 2 for y in [n ** (-1/10)] * len(metric_values)))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Hausdorff Dimension",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
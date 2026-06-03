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
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(1, 2**n) for _ in range(gate_type)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_monotone_width(circuit):
        n = len(circuit)
        width = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            gate_type, inputs = circuit[i]
            if gate_type == 'AND':
                width[i] = max(width[inputs[0]], width[inputs[1]])
            elif gate_type == 'OR':
                width[i] = min(width[inputs[0]], width[inputs[1]])
        return width[0]
    
    def compute_minimal_local_indeterminacy(circuit):
        n = len(circuit)
        indeterminacy = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            gate_type, inputs = circuit[i]
            if gate_type == 'AND':
                indeterminacy[i] = min(indeterminacy[inputs[0]], indeterminacy[inputs[1]])
            elif gate_type == 'OR':
                indeterminacy[i] = max(indeterminacy[inputs[0]], indeterminacy[inputs[1]])
        return indeterminacy[0]
    
    n_max = 40
    instances_tested = 30
    mli_values = []
    w_mon_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_random_circuit(n)
        mli_value = compute_minimal_local_indeterminacy(circuit)
        w_mon_value = compute_monotone_width(circuit)
        mli_values.append(mli_value)
        w_mon_values.append(w_mon_value)
    
    if not mli_values or not w_mon_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_lists"
        }
    
    mean_mli = sum(mli_values) / len(mli_values)
    mean_w_mon = sum(w_mon_values) / len(w_mon_values)
    covariance = sum((mli - mean_mli) * (w_mon - mean_w_mon) for mli, w_mon in zip(mli_values, w_mon_values)) / instances_tested
    variance_mli = sum((mli - mean_mli) ** 2 for mli in mli_values) / instances_tested
    variance_w_mon = sum((w_mon - mean_w_mon) ** 2 for w_mon in w_mon_values) / instances_tested
    pearson_corr = covariance / (math.sqrt(variance_mli) * math.sqrt(variance_w_mon))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
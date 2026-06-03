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
        for _ in range(2**n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate, inputs))
        return circuit
    
    def calculate_monotone_width(circuit):
        n = len(circuit) + 1
        width = [0] * n
        for i in range(n - 1, -1, -1):
            if circuit[i][0] == 'AND':
                width[i] = max(width[circuit[i][1][0]], width[circuit[i][1][1]])
            else:
                width[i] = min(width[circuit[i][1][0]], width[circuit[i][1][1]])
        return width[0]
    
    def calculate_local_indeterminacy(circuit):
        n = len(circuit) + 1
        indeterminacy = [0] * n
        for i in range(n - 1, -1, -1):
            if circuit[i][0] == 'AND':
                indeterminacy[i] = max(indeterminacy[circuit[i][1][0]], indeterminacy[circuit[i][1][1]])
            else:
                indeterminacy[i] = min(indeterminacy[circuit[i][1][0]], indeterminacy[circuit[i][1][1]])
        return indeterminacy[0]
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def correlation(x, y):
        n = len(x)
        x_mean = mean(x)
        y_mean = mean(y)
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = math.sqrt(sum((x[i] - x_mean)**2 for i in range(n)) * sum((y[i] - y_mean)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    lind_values = []
    w_mon_values = []
    
    for n in n_values:
        for _ in range(50):
            circuit = generate_random_circuit(n)
            w_mon = calculate_monotone_width(circuit)
            lind = calculate_local_indeterminacy(circuit)
            lind_values.append(lind)
            w_mon_values.append(w_mon)
    
    correlation_coefficient = correlation(lind_values, w_mon_values)
    mean_lind = mean(lind_values)
    support_fraction = len([x for x in lind_values if 0.5 * w_mon_values[lind_values.index(x)] <= x <= 1.5 * w_mon_values[lind_values.index(x)]] / len(lind_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(lind_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and support_fraction >= 0.5,
        "counterexample": "" if correlation_coefficient >= 0.8 and support_fraction >= 0.5 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")
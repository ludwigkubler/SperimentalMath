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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            inputs = generate_boolean_circuit(n // 2)
            outputs = []
            for i in range(len(inputs) - 1):
                outputs.append(random.choice([inputs[i], inputs[i + 1]]))
            if n % 2 == 1:
                outputs.append(inputs[-1])
            return outputs
    
    def cocomplex(circuit):
        n = len(circuit)
        cocomplex = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            if circuit[i] == 1:
                cocomplex[0][i + 1] = 1
                cocomplex[i + 1][0] = 1
        return cocomplex
    
    def min_rank(cocomplex):
        n = len(cocomplex)
        rank = 0
        for i in range(n):
            if any(cocomplex[j][i] == 1 for j in range(n)):
                rank += 1
        return rank
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(2 ** (n - 1)):
            inputs = [bool(i & (1 << j)) for j in range(n)]
            output = circuit[sum(inputs)]
            if output:
                width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        cocomplex_value = cocomplex(circuit)
        mrank_value = min_rank(cocomplex_value)
        w_mon_value = monotone_width(circuit)
        
        metrics.append({
            "n": n,
            "mrank": mrank_value,
            "w_mon": w_mon_value
        })
    
    instances_tested = len(metrics)
    n_max = max(metric["n"] for metric in metrics)
    
    if n_max < 16:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    correlation_sum = 0
    abs_diff_sum = 0
    
    for metric in metrics:
        correlation_sum += (metric["mrank"] - metric["w_mon"]) * (metric["mrank"] - metric["w_mon"])
        abs_diff_sum += abs(metric["mrank"] - metric["w_mon"])
    
    mean_abs_diff = abs_diff_sum / instances_tested
    if mean_abs_diff > 3:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"mean_abs_diff > 3 ({mean_abs_diff})"
        }
    
    correlation = math.sqrt(correlation_sum / instances_tested)
    if correlation < 0.8:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"correlation < 0.8 ({correlation})"
        }
    
    return {
        "metric_name": "min_rank",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
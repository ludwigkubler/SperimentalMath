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
        if n == 1:
            return ['0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({l} OR {r})' for l in left] + [f'({l} AND {r})' for l in left]
    
    def construct_twistor_space(circuit):
        if not circuit:
            return set()
        elif isinstance(circuit, str) and circuit.isdigit():
            return {circuit}
        else:
            left = construct_twistor_space(circuit[0])
            right = construct_twistor_space(circuit[2])
            return left.union(right)
    
    def min_order(twistor_space):
        if not twistor_space:
            return 0
        return max(len(x) for x in twistor_space)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        twistor_space = construct_twistor_space(circuit)
        o = min_order(twistor_space)
        d = len(circuit.split()) // 2
        results.append((o, d))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_o = sum(o for o, _ in results) / len(results)
    mean_d = sum(d for _, d in results) / len(results)
    covariance = sum((o - mean_o) * (d - mean_d) for o, d in results) / len(results)
    variance_o = sum((o - mean_o) ** 2 for o, _ in results) / len(results)
    variance_d = sum((d - mean_d) ** 2 for _, d in results) / len(results)
    
    if variance_o == 0 or variance_d == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_o) * math.sqrt(variance_d))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.7 and all(pearson_corr >= 0.5 for _ in range(24, 31)),
        "counterexample": "" if pearson_corr >= 0.5 else f"pearson_corr={pearson_corr}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"pearson_corr<0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")
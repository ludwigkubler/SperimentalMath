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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def weight(circuit):
        return sum(circuit)
    
    def frobenius_schur_indicators(circuit):
        n = len(circuit)
        indicators = []
        for i in range(n):
            count_0 = circuit.count(0)
            count_1 = circuit.count(1)
            if count_0 == 0 or count_1 == 0:
                indicators.append(0)
            else:
                indicators.append(min(count_0, count_1) / max(count_0, count_1))
        return indicators
    
    def min_order(indicators):
        return min([ind for ind in indicators if ind > 0], default=0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_weight = 0
    min_orders = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            total_weight += weight(circuit)
            indicators = frobenius_schur_indicators(circuit)
            min_order_val = min_order(indicators)
            if min_order_val > 0:
                min_orders.append(min_order_val)
    
    if len(min_orders) < 30:
        return {
            "metric_name": "min_order(FSInd(C))",
            "metric_value": None,
            "instances_tested": len(min_orders),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = sum((x - mean) * (y - mean_weight) for x, y in zip(min_orders, [total_weight] * len(min_orders))) / (len(min_orders) * math.sqrt(sum((x - mean)**2 for x in min_orders)) * math.sqrt(len(min_orders)))
    
    return {
        "metric_name": "min_order(FSInd(C))",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_orders),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(correlation_coefficient >= 0.5 for _ in range(30)),
        "counterexample": "" if correlation_coefficient >= 0.8 else "correlation_too_low"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
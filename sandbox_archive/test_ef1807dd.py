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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        rank = 1
        while True:
            new_circuit = []
            for i in range(n):
                if circuit[i] != circuit[(i + 1) % n]:
                    new_circuit.append(1)
                else:
                    new_circuit.append(0)
            if len(set(new_circuit)) == 1:
                break
            circuit = new_circuit
            rank += 1
        return rank
    
    def hodge_norm(circuit):
        n = len(circuit)
        count = [0] * (n + 1)
        for i in range(2**n):
            value = sum(circuit[j] * (-1)**j for j in range(n) if i & (1 << j))
            count[abs(value)] += 1
        return min(count[i] / (2**i) for i in range(1, n + 1))
    
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_boolean_circuit(n)
            rank = communication_complexity_rank(circuit)
            norm = hodge_norm(circuit)
            metrics.append((math.log(norm), rank))
            instances_tested += 1
    
    if not metrics:
        return {
            "metric_name": "log(min(H(V_C)))",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_norms, ranks = zip(*metrics)
    correlation_coefficient = sum((log_norms[i] - mean_log_norm) * (ranks[i] - mean_rank) for i in range(len(log_norms))) / math.sqrt(sum((log_norms[i] - mean_log_norm)**2 for i in range(len(log_norms)))) / math.sqrt(sum((ranks[i] - mean_rank)**2 for i in range(len(ranks))))
    mean_log_norm = sum(log_norms) / len(log_norms)
    mean_rank = sum(ranks) / len(ranks)
    
    return {
        "metric_name": "log(min(H(V_C)))",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
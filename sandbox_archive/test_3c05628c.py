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
        # Generate a random circuit of size n
        return [random.randint(1, 3) for _ in range(n)]
    
    def compute_communication_complexity(circuit):
        # Compute the communication complexity rank of the circuit
        # This is a placeholder function; replace with actual computation
        return len(set(circuit))
    
    def compute_monodromy_group_order(curve):
        # Compute the minimal order of monodromy representations for the curve
        # This is a placeholder function; replace with actual computation
        return random.randint(1, 20)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        circuit = generate_circuit(n_max)
        rank = compute_communication_complexity(circuit)
        order = compute_monodromy_group_order(circuit)
        
        if rank > 10 or order > 10:
            return {
                "metric_name": "Monodromy Group Order / Communication Complexity Rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Circuit of size {n_max} with rank {rank} and order {order}"
            }
        
        metric_values.append(order / rank)
    
    mean_metric = sum(metric_values) / instances_tested
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / instances_tested)
    
    return {
        "metric_name": "Monodromy Group Order / Communication Complexity Rank",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(0.95 <= x <= 1.05 for x in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit with rank and order exceeding 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
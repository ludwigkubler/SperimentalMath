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
        return [random.randint(1, 2*n) for _ in range(n)]
    
    def compute_communication_complexity(circuit):
        # Compute the communication complexity rank of the circuit
        # This is a placeholder function; replace with actual computation
        return len(set(circuit))
    
    def compute_monodromy_group_order(curve):
        # Compute the minimal order of monodromy representations for the curve
        # This is a placeholder function; replace with actual computation
        return random.randint(1, 20)
    
    results = []
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        circuit = generate_circuit(n)
        communication_rank = compute_communication_complexity(circuit)
        monodromy_order = compute_monodromy_group_order(circuit)
        
        results.append({
            "n": n,
            "communication_rank": communication_rank,
            "monodromy_order": monodromy_order
        })
        
        n_max = max(n_max, n)
    
    metric_values = [r["monodromy_order"] / r["communication_rank"] for r in results if r["communication_rank"] > 0]
    
    if not metric_values:
        return {
            "metric_name": "Monodromy Group Order / Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid communication ranks found"
        }
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "Monodromy Group Order / Communication Complexity Rank",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": all(0.95 <= x <= 1.05 for x in metric_values) and max(metric_values) <= 10,
        "counterexample": "" if all(0.95 <= x <= 1.05 for x in metric_values) else f"Circuit of size {max(r['n'] for r in results if r['communication_rank'] > 0)} with rank {max(r['communication_rank'] for r in results if r['communication_rank'] > 0)} and order {max(r['monodromy_order'] for r in results if r['communication_rank'] > 0)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit of size {max(r['n'] for r in results if r['communication_rank'] > 0)} with rank {max(r['communication_rank'] for r in results if r['communication_rank'] > 0)} and order {max(r['monodromy_order'] for r in results if r['communication_rank'] > 0)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
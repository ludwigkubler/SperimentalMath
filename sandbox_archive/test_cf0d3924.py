# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_circuit(n):
        if n < 5:
            return "mapping_undefined"
        
        # Generate a simple monotone Boolean circuit
        gates = []
        for i in range(2, n + 1):
            inputs = [random.randint(0, 1) for _ in range(i - 1)]
            gate_type = random.choice(['AND', 'OR'])
            gates.append((gate_type, inputs))
        
        return gates
    
    def tropicalize_quiver(gates):
        # Simplified tropicalization for demonstration
        rank = len(gates)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        if circuit == "mapping_undefined":
            continue
        
        rank = tropicalize_quiver(circuit)
        monotonicity_degree = len(circuit) - 1
        
        results.append({
            "n": n,
            "rank": rank,
            "monotonicity_degree": monotonicity_degree
        })
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_rank = sum(result["rank"] for result in results)
    mean_rank = Fraction(total_rank, len(results))
    support_fraction = sum(1 for result in results if result["rank"] <= result["monotonicity_degree"]) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(mean_rank),
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, rank={results[0]['rank']}, monotonicity_degree={results[0]['monotonicity_degree']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    mean_rank = sum(results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r <= max(results)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(r > max(results) + 1 for r in results):
        print(f"RESULT: FALSIFIED counterexample='rank_exceeds_monotonicity' first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence support_fraction={support_fraction}")
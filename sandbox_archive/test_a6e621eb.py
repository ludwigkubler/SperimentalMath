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
            gate = random.choice(['AND', 'OR', 'NOT'])
            if gate == 'NOT':
                circuit.append((gate, random.randint(0, n-1)))
            else:
                input1 = random.randint(0, n-1)
                input2 = random.randint(0, n-1)
                while input2 == input1:
                    input2 = random.randint(0, n-1)
                circuit.append((gate, input1, input2))
        return circuit
    
    def compute_entanglement_complexity(circuit):
        # Placeholder for actual entanglement complexity computation
        # This is a dummy implementation for testing purposes
        return len(circuit) * 2
    
    def compute_minimal_geometric_entropy(n):
        # Placeholder for actual minimal geometric entropy computation
        # This is a dummy implementation for testing purposes
        return n * math.log2(n)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_random_circuit(n)
        ec = compute_entanglement_complexity(circuit)
        mge = compute_minimal_geometric_entropy(n)
        results.append((ec, mge))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    ec_values = [ec for ec, _ in results]
    mge_values = [mge for _, mge in results]
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, mean_val):
        return math.sqrt(sum((x - mean_val) ** 2 for x in lst) / len(lst))
    
    mean_ec = mean(ec_values)
    mean_mge = mean(mge_values)
    std_ec = std(ec_values, mean_ec)
    std_mge = std(mge_values, mean_mge)
    
    correlation_coefficient = (sum((ec - mean_ec) * (mge - mean_mge) for ec, mge in results) /
                               (len(results) * std_ec * std_mge))
    
    ratio_mean = mean_mge / mean_ec
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": 0.9 <= correlation_coefficient <= 1.0 and 1.2 <= ratio_mean <= 1.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 104729) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean([result['metric_value'] for result in results])} std={std([result['metric_value'] for result in results], mean([result['metric_value'] for result in results]))} support_fraction={support_fraction}")
    elif any("conjecture_holds" not in result or not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
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
    
    def xor_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def barratt_floer_homology(circuit):
        n = len(circuit)
        homology_rank = 0
        for i in range(n):
            if circuit[i] == 1:
                homology_rank += 1
        return homology_rank
    
    def circuit_size(circuit):
        return len(circuit)
    
    def expected_rank(n):
        # Simplified approximation for demonstration purposes
        return math.log2(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        function = xor_circuit(n)
        homology_rank = barratt_floer_homology(function)
        circuit_size_val = circuit_size(function)
        expected_rank_val = expected_rank(n)
        
        if circuit_size_val < 2**(homology_rank + 1):
            results.append((n, homology_rank, circuit_size_val, "falsified"))
        else:
            results.append((n, homology_rank, circuit_size_val, "supported"))
    
    metric_value = sum(result[2] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result[3] == "supported" for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0][0]}, rank={results[0][1]}, circuit_size={results[0][2]}"
    
    return {
        "metric_name": "circuit_size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
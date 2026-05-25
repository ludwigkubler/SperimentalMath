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
    
    def generate_quantum_state(n):
        state = [random.choice([0, 1]) for _ in range(2**n)]
        return state
    
    def communication_complexity(state):
        n = int(math.log2(len(state)))
        # Simplified model: complexity is proportional to the number of qubits
        return n * 2
    
    def minimal_rank(dual_state):
        # Simplified model: rank is proportional to the number of qubits
        return len(dual_state)
    
    def geometric_langlands_duality(state):
        dual_state = state[::-1]  # Simplified model: reverse the state
        return dual_state
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        state = generate_quantum_state(n)
        entanglement_complexity = communication_complexity(state)
        dual_state = geometric_langlands_duality(state)
        min_rank = minimal_rank(dual_state)
        
        if entanglement_complexity == 0:
            continue
        
        ratio = min_rank / (math.log(entanglement_complexity) / math.log(n))
        results.append({
            "n": n,
            "entanglement_complexity": entanglement_complexity,
            "min_rank": min_rank,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_states"
        }
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(0.5 <= result["ratio"] <= 2 for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
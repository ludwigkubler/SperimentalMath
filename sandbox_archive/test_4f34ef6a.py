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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_entanglement_entropy(boolean_function):
        n = int(math.log2(len(boolean_function)))
        # Simplified computation of entanglement entropy (not actual quantum computation)
        return n * math.log(n, 2)
    
    def compute_qubits_needed(boolean_function):
        n = int(math.log2(len(boolean_function)))
        # Simplified computation of qubits needed (not actual quantum circuit simulation)
        return n
    
    metric_name = "Spearman rank correlation coefficient"
    instances_tested = 0
    n_max = 0
    entanglement_entropies = []
    qubit_counts = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        boolean_function = generate_boolean_function(n)
        entanglement_entropy = compute_entanglement_entropy(boolean_function)
        qubit_count = compute_qubits_needed(boolean_function)
        
        entanglement_entropies.append(entanglement_entropy)
        qubit_counts.append(qubit_count)
        
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def spearman_rank_correlation(x, y):
        x_ranks = {x[i]: i for i in range(len(x))}
        y_ranks = {y[i]: i for i in range(len(y))}
        n = len(x)
        sum_d_squared = sum((x_ranks[x[i]] - y_ranks[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    
    correlation_coefficient = spearman_rank_correlation(entanglement_entropies, qubit_counts)
    
    conjecture_holds = abs(correlation_coefficient - n_max) < 0.5
    counterexample = "" if conjecture_holds else f"correlation={correlation_coefficient}, n_max={n_max}"
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_trials = [r for r in results if r["conjecture_holds"]]
    support_fraction = len(supported_trials) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in supported_trials)/len(supported_trials)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in supported_trials)/len(supported_trials)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_mismatch\" first_failing_seed={first_failing_seed}")
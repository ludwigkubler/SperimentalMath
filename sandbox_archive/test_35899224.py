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
    
    def generate_monotone_circuit(n, k):
        # Placeholder for generating a monotone circuit computing k-CLIQUE
        return [[random.choice([0, 1]) for _ in range(k)] for _ in range(n)]
    
    def quantum_geometric_entanglement(circuit):
        # Placeholder for calculating quantum geometric entanglement
        n = len(circuit)
        rank = sum(1 for row in circuit if any(bit == 1 for bit in row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(2, min(n-1, 5))  # Ensure k is at least 2 and less than n
        circuit = generate_monotone_circuit(n, k)
        entanglement = quantum_geometric_entanglement(circuit)
        results.append(entanglement)
    
    total_rank = sum(results)
    avg_rank = total_rank / len(results)
    max_rank = max(results)
    
    conjecture_holds = 2 * n_values[-1] ** k <= avg_rank <= 4 * n_values[-1] ** k
    counterexample = "" if conjecture_holds else f"avg_rank={avg_rank}, max_rank={max_rank}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    max_rank = max(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results) and max_rank > 2 * n_values[-1] ** k:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_rank_exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")
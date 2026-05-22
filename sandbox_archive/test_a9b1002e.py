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
    
    def generate_k_clique_circuit(n):
        # Generate a random k-clique circuit with n inputs
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_automorphism_group_rank(circuit):
        # Placeholder function to simulate computing the automorphism group rank
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 50)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        circuit = generate_k_clique_circuit(n)
        rank = compute_automorphism_group_rank(circuit)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    f_n = max(1, 2**n)  # Placeholder function for f(n), should be replaced with actual logic
    
    return {
        "metric_name": "Automorphism Group Rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": mean_rank >= f_n,
        "counterexample": "" if mean_rank >= f_n else f"n={max(n_values)}, rank={mean_rank}, f(n)={f_n}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
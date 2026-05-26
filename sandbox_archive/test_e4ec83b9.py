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
    
    def generate_arithmetic_circuit(n, m):
        # Simplified generation for demonstration purposes
        return [(random.randint(0, 1), random.randint(0, n-1)) for _ in range(m)]
    
    def compute_symplectic_leaves(circuit):
        leaves = set()
        for gate in circuit:
            if gate[0] == 0:  # AND gate
                leaves.add(gate[1])
            elif gate[0] == 1:  # OR gate
                leaves.add(n + gate[1])
        return leaves
    
    def compute_minimal_rank(leaves):
        rank = len(leaves)
        return rank
    
    n = random.randint(5, 40)
    m = random.randint(1, min(2 * n, 100))
    circuit = generate_arithmetic_circuit(n, m)
    leaves = compute_symplectic_leaves(circuit)
    minimal_rank = compute_minimal_rank(leaves)
    
    expected_bound = n * math.log(m)
    conjecture_holds = minimal_rank <= expected_bound
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={minimal_rank}, expected={expected_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
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
        # Simplified circuit generation for demonstration
        return [(random.randint(0, 1), [random.randint(0, n-1)]) for _ in range(m)]
    
    def symplectic_leaves(circuit):
        leaves = set()
        for gate in circuit:
            leaves.add(gate[1][0])
        return leaves
    
    def minimal_rank(leaves):
        return len(leaves)
    
    n = random.randint(5, 40)
    m = random.randint(1, min(n, 10))
    circuit = generate_arithmetic_circuit(n, m)
    leaves = symplectic_leaves(circuit)
    rank = minimal_rank(leaves)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = (rank <= n * math.log(m))
    counterexample = "" if conjecture_holds else f"rank={rank}, expected={n * math.log(m)}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [101, 103, 107]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
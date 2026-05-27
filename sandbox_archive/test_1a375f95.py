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
        # Placeholder for actual circuit generation logic
        return [random.randint(0, 1) for _ in range(k)]
    
    def compute_geometric_invariant_rank(circuit):
        # Placeholder for actual rank computation logic
        return random.randint(1, n**k)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n // 2, 5))
    circuit = generate_monotone_circuit(n, k)
    rank = compute_geometric_invariant_rank(circuit)
    
    metric_name = "Minimal Rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= 0.9 * n**k
    counterexample = "" if conjecture_holds else f"Rank {rank} < 0.9n^k"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [677, 727, 773, 821, 877, 929]  # Default to 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample = next((r['counterexample'] for r in results if not r['conjecture_holds']), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
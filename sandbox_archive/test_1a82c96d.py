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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        if n == 1:
            return ['x0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({left[0]} OR {right[0]})'] + left + right
    
    def non_archimedean_valuation(circuit):
        if len(circuit) == 1:
            return circuit[0]
        else:
            left = non_archimedean_valuation([circuit[0]])
            right = non_archimedean_valuation(circuit[2:])
            return f'({left} OR {right})'
    
    def minimal_rank(valuation):
        if 'OR' not in valuation:
            return 1
        else:
            left, right = valuation.split(' OR ')
            return max(minimal_rank(left), minimal_rank(right)) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    total_rank = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            valuation = non_archimedean_valuation(circuit)
            rank = minimal_rank(valuation)
            total_instances += 1
            total_rank += rank
    
    mean_rank = Fraction(total_rank, total_instances)
    std_dev = math.sqrt(sum((rank - mean_rank) ** 2 for rank in range(total_rank)) / total_instances)
    
    expected_rank = math.log(n_values[-1], 2)
    within_1_std_dev = abs(mean_rank - expected_rank) <= std_dev
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": total_instances,
        "conjecture_holds": within_1_std_dev,
        "counterexample": "" if within_1_std_dev else f"Expected rank {expected_rank}, got {mean_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
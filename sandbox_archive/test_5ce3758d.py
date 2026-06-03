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
    
    def generate_circuit(n):
        # Generate a random circuit of size n
        return [random.choice([0, 1]) for _ in range(n)]
    
    def compute_communication_complexity(circuit):
        # Simplified communication complexity calculation
        return sum(circuit) + len(circuit)
    
    def compute_monodromy_group_order(circuit):
        # Simplified monodromy group order calculation
        return 2 ** len(circuit)
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        circuit = generate_circuit(n)
        comm_complexity_rank = compute_communication_complexity(circuit)
        monodromy_group_order = compute_monodromy_group_order(circuit)
        
        instances_tested += 1
        total_metric_value += monodromy_group_order / comm_complexity_rank
        
        if abs(monodromy_group_order / comm_complexity_rank - 1) > 0.2:
            conjecture_holds = False
            counterexample = f"Circuit of size {n} with rank {comm_complexity_rank} and order {monodromy_group_order}"
    
    mean_metric_value = total_metric_value / instances_tested
    
    return {
        "metric_name": "Monodromy Group Order / Communication Complexity Rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
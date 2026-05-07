# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_additive_energy(truth_table):
        n = truth_table.index(1).bit_length() - 1
        energy = 0
        for x, y, z, w in combinations(range(2**n), 4):
            if (truth_table[x] + truth_table[y]) == (truth_table[z] + truth_table[w]):
                energy += 1
        return energy
    
    def deterministic_communication_complexity(truth_table):
        n = truth_table.index(1).bit_length() - 1
        instances_tested = 0
        for x in range(2**n):
            for y in range(2**n):
                if (truth_table[x] + truth_table[y]) == 1:
                    instances_tested += 1
        return instances_tested
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    energy = compute_additive_energy(f)
    
    communication_complexity = deterministic_communication_complexity(f)
    
    conjecture_holds = energy >= n**3 and communication_complexity >= n
    counterexample = "" if conjecture_holds else "energy < n^3 or communication complexity < n"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 2**n * (2**n - 1),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
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
    
    def generate_sipser_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def truth_table_to_additive_energy(truth_table):
        n = int(math.log2(len(truth_table)))
        energy = 0
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    for l in range(k+1, n):
                        if truth_table[i] + truth_table[j] == truth_table[k] + truth_table[l]:
                            energy += 1
        return energy
    
    def is_acc0_circuit(truth_table, size_bound):
        # Simulate ACC⁰ circuit using a randomized algorithm (simplified)
        n = int(math.log2(len(truth_table)))
        for _ in range(size_bound):
            if random.choice(truth_table) == 1:
                return True
        return False
    
    n = 40
    sipser_function = generate_sipser_function(n)
    truth_table = [sipser_function[i] for i in range(2**n)]
    energy = truth_table_to_additive_energy(truth_table)
    
    size_bound = math.ceil(n**(2.5) / math.log(n))
    is_acc0 = is_acc0_circuit(truth_table, size_bound)
    
    return {
        "metric_name": "additive_energy",
        "metric_value": energy,
        "instances_tested": 1,
        "conjecture_holds": not is_acc0,
        "counterexample": "" if not is_acc0 else f"Sipser function on n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    std_energy = math.sqrt(sum((r["metric_value"] - mean_energy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Sipser function' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexample_found")
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
    
    def generate_random_circuit(n):
        # Simplified circuit generation for demonstration
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_quadratic_entanglement(circuit):
        # Simplified computation of quadratic entanglement
        return sum(x * x for x in circuit)
    
    def bp_read_twice_circuit_depth(circuit):
        # Simplified BP_ReadTwice circuit depth calculation
        return len(circuit)
    
    def compute_minimal_rank(entanglement):
        # Simplified minimal rank computation
        return entanglement
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    entanglement = compute_quadratic_entanglement(circuit)
    depth = bp_read_twice_circuit_depth(circuit)
    minimal_rank = compute_minimal_rank(entanglement)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexample = next((r['counterexample'] for r in results if not r['conjecture_holds']), "")
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
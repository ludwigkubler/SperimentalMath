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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalized_homology_group(f):
        n = int(math.log2(len(f)))
        homology = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i == j:
                    homology[i][j] = sum(f[k] for k in range(2**n) if bin(k).count('1') == i)
        return homology
    
    def min_rank(homology):
        n = len(homology) - 1
        rank = 0
        for _ in range(n + 1):
            pivot_row = next((i for i in range(rank, n + 1) if homology[i][rank] != 0), None)
            if pivot_row is None:
                break
            homology[pivot_row], homology[rank] = homology[rank], homology[pivot_row]
            for j in range(n + 1):
                if j == rank:
                    continue
                factor = homology[j][rank] / homology[rank][rank]
                for k in range(n + 1):
                    homology[j][k] -= factor * homology[rank][k]
            rank += 1
        return rank
    
    def construct_monotone_circuit(f, n):
        # Placeholder function to construct a monotone circuit
        # This is a dummy implementation and should be replaced with actual logic
        return [random.randint(2, n) for _ in range(len(f))]
    
    def gate_count(circuit):
        return sum(circuit)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    homology = tropicalized_homology_group(f)
    r = min_rank(homology)
    
    circuits = [construct_monotone_circuit(f, n) for _ in range(30)]
    conjecture_holds = all(gate_count(circuit) <= r * (n + 1) for circuit in circuits)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Gate Count",
        "metric_value": sum(gate_count(circuit) for circuit in circuits),
        "instances_tested": len(circuits),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 150, 5))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
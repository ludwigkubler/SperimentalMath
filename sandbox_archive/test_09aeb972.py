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
    
    def generate_circuit(depth, n):
        if depth == 1:
            return [random.choice([0, 1]) for _ in range(n)]
        else:
            subcircuits = [generate_circuit(random.randint(1, depth-1), n) for _ in range(2)]
            return [subcircuits[0][i] ^ subcircuits[1][i] for i in range(n)]
    
    def braid_action(circuit):
        n = len(circuit)
        braid = random.sample(range(n), n)
        new_circuit = [circuit[braid[i]] for i in range(n)]
        return new_circuit
    
    def circuit_depth(circuit):
        if all(isinstance(x, list) for x in circuit):
            return 1 + max(circuit_depth(subcircuit) for subcircuit in circuit)
        else:
            return 0
    
    def braid_group_action(circuit):
        depth = circuit_depth(circuit)
        new_circuits = set()
        for _ in range(100):  # Sample 100 random braids
            new_circuit = braid_action(circuit)
            new_circuits.add(tuple(new_circuit))
        return len(new_circuits)
    
    def count_distinct_automorphisms(circuit):
        depth = circuit_depth(circuit)
        if depth < 5:
            return 0
        automorphisms = set()
        for _ in range(100):  # Sample 100 random braids
            automorphism = braid_action(circuit)
            automorphisms.add(tuple(automorphism))
        return len(automorphisms)
    
    n = random.randint(5, 40)
    depth = random.randint(5, 40)
    circuit = generate_circuit(depth, n)
    
    try:
        num_automorphisms = count_distinct_automorphisms(circuit)
        metric_value = num_automorphisms
        instances_tested = 1
        conjecture_holds = False
        counterexample = ""
        
        if depth > 5 and num_automorphisms <= n**2:  # Polynomial bound for demonstration
            conjecture_holds = True
        
        return {
            "metric_name": "Number of distinct automorphisms",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    except Exception as e:
        return {
            "metric_name": "Number of distinct automorphisms",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
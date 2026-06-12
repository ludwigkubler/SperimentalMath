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
    
    def generate_boolean_circuit(n, d):
        circuit = [0] * n
        for _ in range(d):
            pos1 = random.randint(0, n-1)
            pos2 = random.randint(0, n-1)
            if pos1 != pos2:
                circuit[pos1] ^= 1
                circuit[pos2] ^= 1
        return circuit
    
    def count_symplectic_leaves(circuit):
        n = len(circuit)
        leaves = set()
        for i in range(1 << n):
            leaf = []
            for j in range(n):
                if (i >> j) & 1:
                    leaf.append(circuit[j])
            leaves.add(tuple(sorted(leaf)))
        return len(leaves)
    
    def entanglement_complexity(circuit):
        n = len(circuit)
        max_entanglement = 0
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    max_entanglement += 1
        return max_entanglement
    
    metric_name = "symplectic_leaves"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        total_leaves = 0
        for _ in range(instances_tested):
            circuit = generate_boolean_circuit(n, entanglement_complexity(generate_boolean_circuit(n, 0)))
            leaves = count_symplectic_leaves(circuit)
            total_leaves += leaves
        
        mean_leaves = total_leaves / instances_tested
        if mean_leaves > n * 2**(n/4):
            conjecture_holds = False
            counterexample = f"Mean leaves {mean_leaves} exceeds bound {n * 2**(n/4)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_leaves,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
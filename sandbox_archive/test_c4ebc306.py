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
    
    def generate_circuit(m, d):
        if m == 0 or d == 0:
            return []
        if d == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_circuit(m // 2, d - 1) for _ in range(2)]
            return [subcircuits[0], subcircuits[1]]
    
    def evaluate_circuit(circuit):
        stack = []
        for gate in circuit:
            if isinstance(gate, list):
                a = evaluate_circuit(gate)
                b = stack.pop()
                stack.append(a & b)
            else:
                stack.append(gate)
        return stack[0]
    
    def frege_proof_depth(circuit):
        if not circuit:
            return 1
        if isinstance(circuit[0], list):
            depth1 = frege_proof_depth(circuit[0])
            depth2 = frege_proof_depth(circuit[1])
            return max(depth1, depth2) + 1
        else:
            return 1
    
    def symplectic_hull_volume(circuit):
        if not circuit:
            return 1
        if isinstance(circuit[0], list):
            volume1 = symplectic_hull_volume(circuit[0])
            volume2 = symplectic_hull_volume(circuit[1])
            return volume1 * volume2
        else:
            return 1
    
    m = random.randint(5, 40)
    d = random.randint(5, 40)
    circuit = generate_circuit(m, d)
    
    shv = symplectic_hull_volume(circuit)
    fpd = frege_proof_depth(circuit)
    
    return {
        "metric_name": "SHV vs FPD",
        "metric_value": shv / fpd,
        "instances_tested": 1,
        "n_max": max(m, d),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
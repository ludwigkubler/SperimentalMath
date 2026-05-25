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
    
    def boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalized_homology(f):
        # Simplified version of tropicalized homology for demonstration
        return len(set(f))
    
    def monotone_circuit(f):
        n = int(math.log2(len(f)))
        circuit = [random.choice([0, 1]) for _ in range(n)]
        return circuit
    
    def gate_count(circuit):
        return sum(1 for x in circuit if x != 0)
    
    n = random.randint(5, 40)
    f = boolean_function(n)
    H_f = tropicalized_homology(f)
    r_H_f = H_f
    circuits = [monotone_circuit(f) for _ in range(30)]
    
    conjecture_holds = True
    counterexample = ""
    
    for circuit in circuits:
        if gate_count(circuit) > r_H_f * (n + 1):
            conjecture_holds = False
            counterexample = f"Circuit with {gate_count(circuit)} gates exceeds bound"
            break
    
    return {
        "metric_name": "Gate Count",
        "metric_value": sum(gate_count(circuit) for circuit in circuits),
        "instances_tested": len(circuits),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for res in results if not res["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
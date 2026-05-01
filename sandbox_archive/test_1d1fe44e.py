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
    
    # Define the tropical circuit and its dual
    def create_tropical_circuit(n):
        circuit = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        return circuit
    
    def duality_flip(circuit):
        n = len(circuit)
        dual_circuit = [[circuit[j][i] for j in range(n)] for i in range(n)]
        return dual_circuit
    
    # Define homotopy stability check
    def is_homotopy_stable(circuit, epsilon=1e-6):
        n = len(circuit)
        original_solution = [sum(row[i] for row in circuit) for i in range(n)]
        perturbed_circuit = [[c + random.uniform(-epsilon, epsilon) if c != 0 else c for c in row] for row in circuit]
        perturbed_solution = [sum(row[i] for row in perturbed_circuit) for i in range(n)]
        return all(abs(original_solution[i] - perturbed_solution[i]) <= epsilon for i in range(n))
    
    # Create a tropical circuit and its dual
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = create_tropical_circuit(n)
    dual_circuit = duality_flip(circuit)
    
    # Check homotopy stability for both circuits
    original_stable = is_homotopy_stable(circuit)
    dual_stable = is_homotopy_stable(dual_circuit)
    
    return {
        "metric_name": "homotopy_stability",
        "metric_value": 1 if original_stable and dual_stable else 0,
        "instances_tested": 2,
        "conjecture_holds": original_stable and dual_stable,
        "counterexample": "" if original_stable and dual_stable else "Solution difference exceeds epsilon"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Solution difference exceeds epsilon\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
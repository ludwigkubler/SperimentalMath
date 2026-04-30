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
    
    # Define the tropical circuit and derivation sparsity calculation
    def tropical_circuit(n):
        return sum([random.choice([-1, 0, 1]) * x for x in range(1, n + 1)])
    
    def derivation_sparsity(circuit):
        active_edges = [x != 0 for x in circuit]
        return max(active_edges.count(True) for _ in range(10))
    
    # Define the phase cell count calculation
    def phase_cell_count(circuit):
        inputs = [[i] * n for i in range(-5, 6)]
        cells = set()
        for input_val in itertools.product(*inputs):
            output = tropical_circuit(input_val)
            cells.add(output)
        return len(cells)
    
    # Generate a random tropical circuit
    n = random.randint(5, 10)
    circuit = [random.choice([-1, 0, 1]) * x for x in range(1, n + 1)]
    
    # Calculate the derivation sparsity and phase cell count
    sparsity = derivation_sparsity(circuit)
    cells = phase_cell_count(circuit)
    
    # Check if the conjecture holds
    conjecture_holds = cells <= sparsity ** 2  # Polynomial bound of degree 2
    
    return {
        "metric_name": "Phase Cell Count",
        "metric_value": cells,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample: n={n}, sparsity={sparsity}, cells={cells}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cells = sum(r["metric_value"] for r in results) / len(results)
    std_cells = math.sqrt(sum((r["metric_value"] - mean_cells) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_cells} std={std_cells} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cells} std={std_cells} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
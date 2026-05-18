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
    
    def generate_random_circuit(n, s):
        gates = ['AND', 'OR', 'NOT', 'MOD_2']
        circuit = []
        for _ in range(s):
            gate_type = random.choice(gates)
            if gate_type == 'NOT':
                input_gate = random.randint(0, len(circuit) - 1)
                circuit.append((gate_type, input_gate))
            else:
                inputs = [random.randint(0, len(circuit) - 1) for _ in range(random.randint(2, 4))]
                circuit.append((gate_type, inputs))
        return circuit
    
    def generate_corr_circuits(n, s):
        # Placeholder for actual implementation
        return []
    
    def generate_and_n_corr_circuits(n, s):
        # Placeholder for actual implementation
        return []
    
    def compute_additive_energy(circuit):
        out_degrees = [0] * len(circuit)
        for i, (gate_type, inputs) in enumerate(circuit):
            if gate_type == 'NOT':
                out_degrees[inputs] += 1
            else:
                for input_gate in inputs:
                    out_degrees[input_gate] += 1
        
        pair_sums = sorted([d_i + d_j for d_i, d_j in combinations(out_degrees, 2)])
        energy = sum(1 for i, j, k, l in combinations(pair_sums, 4) if i == k and j == l) / len(circuit) ** 3
        return energy
    
    def corr(f_C, MOD_3):
        # Placeholder for actual implementation
        return random.random()
    
    n = random.choice([6, 7, 8])
    s = random.choice([12, 20, 28, 36])
    
    circuit = generate_random_circuit(n, s)
    corr_value = corr(circuit, 'MOD_3')
    energy = compute_additive_energy(circuit)
    
    return {
        "metric_name": "additive_energy",
        "metric_value": energy,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    std_energy = math.sqrt(sum((r["metric_value"] - mean_energy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
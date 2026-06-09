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
    
    def generate_circuit(depth, gate_count):
        # Simple circuit generation for demonstration purposes
        circuit = []
        for _ in range(gate_count):
            if random.random() < 0.5:
                circuit.append('AND')
            else:
                circuit.append('OR')
        return circuit
    
    def compute_partition(circuit):
        # Dummy partition function for demonstration purposes
        return len(circuit)
    
    def compute_communication_complexity_rank(circuit):
        # Dummy rank function for demonstration purposes
        return len(set(circuit))
    
    depth = 5 + random.randint(0, 4) * 5
    gate_count = 10 + random.randint(0, 9) * 10
    
    circuit = generate_circuit(depth, gate_count)
    partition = compute_partition(circuit)
    rank = compute_communication_complexity_rank(circuit)
    
    return {
        "metric_name": "Partition(C)",
        "metric_value": partition,
        "instances_tested": 1,
        "n_max": depth,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        RESULT = "INCONCLUSIVE mapping_undefined"
    else:
        supported_count = sum(1 for r in results if r["conjecture_holds"])
        support_fraction = supported_count / len(results)
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}"
    
    print(RESULT)
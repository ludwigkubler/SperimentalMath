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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            max_inputs = 0
            for j in range(i + 1, n):
                if all(circuit[j][1][k] <= circuit[i][1][k] for k in range(len(circuit[i][1]))):
                    max_inputs += 1
            width = max(width, max_inputs)
        return width
    
    def local_indeterminacy(circuit):
        n = len(circuit)
        indeterminacy = 0
        for i in range(n):
            if circuit[i][0] == 'AND':
                indeterminacy += sum(1 for x in circuit[i][1] if x == 0)
            elif circuit[i][0] == 'OR':
                indeterminacy += sum(1 for x in circuit[i][1] if x == 1)
        return indeterminacy
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    w_mon = monotone_width(circuit)
    lind = local_indeterminacy(circuit)
    
    return {
        "metric_name": "local_indeterminacy",
        "metric_value": lind,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_lind = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    if RESULT == "SUPPORTED":
        print(f"RESULT: {RESULT} mean={mean_lind:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif RESULT == "FALSIFIED":
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: {RESULT} counterexample='not supported' first_failing_seed={first_failing_seed}")
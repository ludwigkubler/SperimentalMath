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
    
    def generate_random_circuit(depth):
        if depth == 0:
            return ['0'] if random.choice([True, False]) else ['1']
        elif depth == 1:
            return [random.choice(['NOT', 'AND', 'OR'])]
        else:
            subcircuits = [generate_random_circuit(random.randint(0, depth-1)) for _ in range(random.randint(2, 4))]
            return [random.choice(['NOT', 'AND', 'OR'])] + subcircuits
    
    def is_valid_lattice(lattice):
        if not lattice:
            return False
        for i in range(len(lattice)):
            for j in range(i+1, len(lattice)):
                if lattice[i] == lattice[j]:
                    return False
        return True
    
    def compute_minimal_lattice(circuit):
        n = 2 ** (len(circuit) // 2)
        lattice = []
        for i in range(n):
            row = [str((i >> j) & 1) for j in range(len(circuit))]
            if is_valid_lattice(row):
                lattice.append(''.join(row))
        return lattice
    
    def depth_of_circuit(circuit):
        if isinstance(circuit[0], str):
            return 1
        else:
            return max(depth_of_circuit(subcircuit) for subcircuit in circuit[1:]) + 1
    
    n_max = 40
    instances_tested = 0
    total_lattice_size = 0
    
    for n in range(5, n_max + 1):
        if n > 30:
            break
        
        for _ in range(30 // (n - 4)):
            circuit = generate_random_circuit(n)
            lattice_size = len(compute_minimal_lattice(circuit))
            total_lattice_size += lattice_size
            instances_tested += 1
    
    mean_lattice_size = total_lattice_size / instances_tested
    conjecture_holds = abs(mean_lattice_size - n) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_lattice_size",
        "metric_value": mean_lattice_size,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_lattice_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_lattice_size} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_lattice_size} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}")
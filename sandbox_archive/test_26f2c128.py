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
    
    def generate_circuit(n, D, G):
        # Simplified circuit generation for demonstration
        circuit = []
        for _ in range(G):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate_type, inputs))
        return circuit
    
    def partition(circuit, n):
        # Simplified partitioning logic for demonstration
        partitions = {}
        for i in range(n):
            partitions[i] = [i]
        return partitions
    
    def communication_complexity_rank(partitions):
        # Simplified rank calculation for demonstration
        return len(partitions)
    
    n = random.randint(5, 30)
    D = random.randint(1, 3)
    G = random.randint(10, 20)
    circuit = generate_circuit(n, D, G)
    partitions = partition(circuit, n)
    r_C = communication_complexity_rank(partitions)
    
    return {
        "metric_name": "Partition(C)",
        "metric_value": len(partitions),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
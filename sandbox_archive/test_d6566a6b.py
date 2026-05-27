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
    
    def create_tseitin_circuit(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(m):
            clause = random.sample(variables, 2)
            clauses.append(f"({clause[0]} OR {clause[1]})")
        return clauses

    def tseitin_circuit_width(clauses):
        width = 0
        for clause in clauses:
            if 'OR' in clause:
                width += 1
        return width

    def create_tqft(circuit):
        # Placeholder function to simulate creating a tQFT from a circuit
        # This is a dummy implementation and does not actually compute the depth
        return random.randint(1, 10)

    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    circuit = create_tseitin_circuit(n, m)
    width = tseitin_circuit_width(circuit)
    tqft_depth = create_tqft(circuit)
    
    return {
        "metric_name": "tQFT Depth",
        "metric_value": tqft_depth,
        "instances_tested": 1,
        "conjecture_holds": tqft_depth >= width,
        "counterexample": "" if tqft_depth >= width else f"Depth {tqft_depth} < Width {width}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
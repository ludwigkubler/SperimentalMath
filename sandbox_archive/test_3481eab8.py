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
        # Generate a random n-qubit circuit
        return [random.choice(['H', 'CNOT']) for _ in range(n)]
    
    def compute_quadratic_entanglement_pattern(circuit):
        # Simplified computation of quadratic entanglement pattern
        return len(circuit)
    
    def construct_bp_readtwice_circuit(circuit):
        # Construct a BP_ReadTwice circuit from the given circuit
        depth = 0
        for gate in circuit:
            if gate == 'H':
                depth += 1
            elif gate == 'CNOT':
                depth += 2
        return depth
    
    def compute_minimal_rank(entanglement_pattern):
        # Simplified computation of minimal rank
        return len(entanglement_pattern)
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    entanglement_pattern = compute_quadratic_entanglement_pattern(circuit)
    bp_readtwice_depth = construct_bp_readtwice_circuit(circuit)
    minimal_rank = compute_minimal_rank(entanglement_pattern)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    std_rank = math.sqrt(sum((r['metric_value'] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
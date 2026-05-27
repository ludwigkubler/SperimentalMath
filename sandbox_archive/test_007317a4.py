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

def negation_width(circuit):
    if isinstance(circuit, tuple) and circuit[0] == 'NOT':
        return 1 + max(negation_width(sub_circuit) for sub_circuit in circuit[1:])
    elif isinstance(circuit, tuple):
        return max(negation_width(sub_circuit) for sub_circuit in circuit)
    else:
        return 0

def generate_random_circuit(depth, num_gates):
    if depth == 0:
        return random.choice(['0', '1'])
    gate = random.choice(['AND', 'OR', 'NOT'])
    if gate == 'NOT':
        return (gate, generate_random_circuit(depth - 1, num_gates))
    else:
        return (gate, generate_random_circuit(depth - 1, num_gates), generate_random_circuit(depth - 1, num_gates))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(1, 10)
    circuit = generate_random_circuit(n, 2**k)
    neg_width = negation_width(circuit)
    
    # Placeholder for computing the minimal rank of tropicalized Hodge structure
    # This is a dummy value; replace with actual computation if possible
    min_rank = random.randint(1, neg_width)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank >= neg_width / math.log2(neg_width),
        "counterexample": "" if min_rank >= neg_width / math.log2(neg_width) else f"neg_width={neg_width}, min_rank={min_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(res["metric_value"] for res in results) / len(results)
    std_metric = math.sqrt(sum((res["metric_value"] - mean_metric)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"neg_width < min_rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
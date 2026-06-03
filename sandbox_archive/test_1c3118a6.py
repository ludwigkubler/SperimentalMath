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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_circuit(depth, size):
    if depth == 0:
        return [random.choice([True, False])]
    else:
        subcircuits = [generate_circuit(depth-1, size//2) for _ in range(2)]
        circuit = []
        for sc in subcircuits:
            circuit.extend(sc)
        while len(circuit) < size:
            circuit.append(random.choice([True, False]))
        return circuit

def compute_entropy(circuit):
    counts = {False: 0, True: 0}
    for bit in circuit:
        counts[bit] += 1
    total = len(circuit)
    p_true = Fraction(counts[True], total)
    p_false = Fraction(counts[False], total)
    if p_true == 0 or p_false == 0:
        return 0
    entropy = -p_true * math.log2(p_true) - p_false * math.log2(p_false)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(random.randint(1, 4), n)
            entropy = compute_entropy(circuit)
            metric_values.append(entropy)
            instances_tested += 1
            n_max = max(n_max, len(circuit))

    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5

    if any(entropy <= 0 for entropy in metric_values):
        conjecture_holds = False
        counterexample = "non-positive entropy"

    return {
        "metric_name": "Minimal Topological Entropy",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
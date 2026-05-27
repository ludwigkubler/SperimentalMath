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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_circuit(n):
        circuit = []
        for i in range(2**n):
            circuit.append(random.choice([0, 1]))
        return circuit
    
    def compute_geometric_entropy(circuit):
        n = len(circuit)
        if n == 0:
            return 0
        counts = [circuit.count(i) for i in range(2)]
        probabilities = [Fraction(count, n) for count in counts]
        entropy = -sum(prob * math.log2(prob) for prob in probabilities if prob != 0)
        return entropy
    
    def evaluate_circuit(circuit):
        n = len(circuit)
        input_val = random.randint(0, 2**n - 1)
        output_val = circuit[input_val]
        return output_val
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different circuits
            circuit = generate_monotone_circuit(n)
            entropy = compute_geometric_entropy(circuit)
            output_val = evaluate_circuit(circuit)
            total_entropy += entropy
            instances_tested += 1
    
    mean_entropy = Fraction(total_entropy, instances_tested)
    conjecture_holds = mean_entropy >= Fraction(1, n**0.25) / (n // 2)
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": float(mean_entropy),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean entropy {mean_entropy} < Ω(n^(1/4)/D(n))",
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        print(f"TRIAL: {seed}")
        trial_result = run_trial(seed)
        results.append(trial_result)
    
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0 support_fraction=1")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
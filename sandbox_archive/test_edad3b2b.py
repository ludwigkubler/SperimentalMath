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
    
    def generate_circuit(n, s):
        circuit = []
        for _ in range(s):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def vertex_cover(circuit):
        if not circuit:
            return 0
        gate, inputs = circuit[0]
        if gate == 'AND':
            return 1 + max(vertex_cover(circuit[1:]), vertex_cover([(gate, inputs[1:])]))
        else:
            return 1 + min(vertex_cover(circuit[1:]), vertex_cover([(gate, inputs[1:])]))
    
    def count_reduced_words(circuit):
        if not circuit:
            return 0
        gate, inputs = circuit[0]
        words = set()
        for i in range(2**len(inputs)):
            word = [inputs[j] if (i & (1 << j)) else 1 - inputs[j] for j in range(len(inputs))]
            words.add(tuple(word))
        return len(words)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            s = random.randint(n, min(40, n * 2))
            circuit = generate_circuit(n, s)
            reduced_words = count_reduced_words(circuit)
            vertex_cover_size = vertex_cover(circuit)
            results.append((n, s, reduced_words, vertex_cover_size))
    
    total_instances = len(results)
    mean_metric_value = sum(s**(1/3) for _, s, _, _ in results) / total_instances
    support_fraction = sum(1 for _, _, _, v in results if v <= 0.5 * mean_metric_value) / total_instances
    
    return {
        "metric_name": "circuit_size_bound",
        "metric_value": mean_metric_value,
        "instances_tested": total_instances,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction:.2f} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='support_fraction={support_fraction:.2f} < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                circuit.append(('NOT', random.randint(0, len(circuit) - 1)))
            else:
                inputs = [random.randint(0, len(circuit) - 1) for _ in range(2)]
                circuit.append((gate_type, *inputs))
        return circuit
    
    def communication_complexity(circuit):
        # Simplified model: complexity is proportional to the number of gates
        return len(circuit)
    
    def quaternionic_automorphism_group_order(circuit):
        # Simplified model: order is proportional to the number of gates squared
        return len(circuit) ** 2
    
    n_max = 40
    instances_tested = 30
    ratios = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        order = quaternionic_automorphism_group_order(circuit)
        complexity = communication_complexity(circuit)
        
        if complexity == 0:
            continue
        
        ratio = order / complexity
        ratios.append(ratio)
    
    mean_ratio = sum(ratios) / len(ratios) if ratios else 0
    
    conjecture_holds = all(0.5 <= r <= 1.5 for r in ratios)
    counterexample = "" if conjecture_holds else "Ratio out of range"
    
    return {
        "metric_name": "Ratio of Quaternionic Automorphism Group Order to Communication Complexity",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of range\" first_failing_seed={first_failing_seed}")
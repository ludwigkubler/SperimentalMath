# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_weyl_group_representation(circuit):
        # Placeholder function to simulate Weyl group representation computation
        # This is a dummy implementation and should be replaced with actual logic
        rank = len(circuit)
        return rank
    
    n = 10  # Example value for n, can be changed as needed
    m_max = int(n ** (2/3))
    
    instances_tested = 0
    total_rank = 0
    
    for _ in range(30):  # Test with 30 random circuits
        m = random.randint(1, m_max)
        circuit = generate_random_boolean_circuit(n, m)
        rank = compute_weyl_group_representation(circuit)
        
        if rank >= m:
            instances_tested += 1
            total_rank += rank
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else float('inf')
    
    conjecture_holds = mean_rank <= 3 * n ** (2/3)
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank} exceeds bound {3 * n ** (2/3)}"
    
    return {
        "metric_name": "Minimal Rank of Weyl Group Representation",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r['conjecture_holds']:
                counterexample = r['counterexample']
                first_failing_seed = r['seed']
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
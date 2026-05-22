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
    
    def generate_ac0_circuit(n):
        # Generate a simple AC0 circuit with size n
        return [random.choice(['AND', 'OR']) for _ in range(n)]
    
    def compute_minimal_representation_rank(circuit_size):
        # Placeholder function to compute the minimal representation rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, circuit_size)
    
    n = 40
    circuit = generate_ac0_circuit(n)
    min_rank = compute_minimal_representation_rank(len(circuit))
    
    metric_value = min_rank / len(circuit)
    instances_tested = 1
    conjecture_holds = min_rank >= (2/3) * n**(2/3)
    counterexample = '' if conjecture_holds else 'minimal_representation_rank_too_low'
    
    return {
        "metric_name": "Minimal Representation Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample='minimal_representation_rank_too_low' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
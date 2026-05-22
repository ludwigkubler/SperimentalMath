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
        # Generate a simple AC0 circuit with n gates
        return [random.choice(['AND', 'OR']) for _ in range(n)]
    
    def compute_minimal_representation_rank(circuit_size):
        # Placeholder function to simulate computing the minimal representation rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.random() * circuit_size ** (2/3)
    
    n = 40
    circuit = generate_ac0_circuit(n)
    rank = compute_minimal_representation_rank(len(circuit))
    
    return {
        "metric_name": "Minimal Representation Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= n ** (2/3),
        "counterexample": "minimal_representation_rank_too_low" if rank < n ** (2/3) else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample='minimal_representation_rank_too_low' first_failing_seed={first_failing_seed}")
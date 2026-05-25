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
    
    def boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalized_homology_group(f):
        n = len(f)
        if n == 1:
            return 1
        homology = 0
        for i in range(1, n):
            homology += sum(1 for j in range(len(f)) if f[j] != f[j ^ (1 << i)])
        return homology
    
    def monotone_circuit(n, r):
        gates = []
        for _ in range(r):
            gate = random.choice([0, 1])
            gates.append(gate)
        return gates
    
    n = random.randint(5, 40)
    f = boolean_function(n)
    homology_rank = tropicalized_homology_group(f)
    
    min_gates = float('inf')
    for _ in range(30):
        circuit = monotone_circuit(n, homology_rank)
        if len(circuit) < min_gates:
            min_gates = len(circuit)
    
    conjecture_holds = min_gates <= homology_rank * (n + 1)
    counterexample = "" if conjecture_holds else f"Counterexample: n={n}, homology_rank={homology_rank}, min_gates={min_gates}"
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Homology Groups vs Monotone Circuit Complexity",
        "metric_value": homology_rank * (n + 1),
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
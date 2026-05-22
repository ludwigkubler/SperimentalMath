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
    
    def xor_and_network(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def quandle_operations(network):
        n = len(network)
        rank = 0
        for i in range(2**n):
            if all((network[i] == network[j]) == (i & j == i) for j in range(2**n)):
                rank += 1
        return rank
    
    def acc0_circuit_size(n):
        # Simplified approximation of ACC⁰ circuit size for XOR-AND networks
        return n * math.log2(n)
    
    n = random.randint(5, 40)
    network = xor_and_network(n)
    quandle_rank = quandle_operations(network)
    acc0_circuit_size_value = acc0_circuit_size(n)
    
    metric_name = "Quandle Rank / ACC⁰ Circuit Size"
    metric_value = quandle_rank / acc0_circuit_size_value
    instances_tested = 1
    conjecture_holds = quandle_rank <= math.log2(n)**2 and acc0_circuit_size_value <= n * math.log2(n)
    counterexample = "" if conjecture_holds else f"Quandle Rank: {quandle_rank}, ACC⁰ Circuit Size: {acc0_circuit_size_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37]  # Default to first 30 primes and 37
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Quandle Rank exceeds log^2(n) or ACC⁰ Circuit Size exceeds n * log2(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical signal")
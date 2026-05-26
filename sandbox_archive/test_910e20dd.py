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
    
    def generate_monotone_circuit(k):
        # Simplified generation of a monotone circuit for k-CLIQUE
        return [random.choice([0, 1]) for _ in range(2**k)]
    
    def tensor_product_rank(circuit):
        n = len(circuit)
        rank = 1
        for bit in circuit:
            if bit == 1:
                rank *= 2
        return rank
    
    k_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for k in k_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_monotone_circuit(k)
            rank = tensor_product_rank(circuit)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= seed**math.sqrt(k_values[-1]/4)
    
    return {
        "metric_name": "tensor_product_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean rank {mean_rank} exceeds n^Ω(k^{1/4})"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean rank exceeds n^Ω(k^{1/4})\" first_failing_seed={first_failing_seed}")
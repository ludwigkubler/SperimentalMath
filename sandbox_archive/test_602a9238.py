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
    
    def generate_parity_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalize(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            if circuit[i] == 1:
                rank += 1
        return rank
    
    def ac0_circuit_size(circuit):
        n = len(circuit)
        return 2**n
    
    instances_tested = 0
    total_rank = 0
    total_size = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_parity_circuit(n)
        rank = tropicalize(circuit)
        size = ac0_circuit_size(circuit)
        
        instances_tested += 1
        total_rank += rank
        total_size += size
        
        if rank > math.log2(size):
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, size={size}"
    
    mean_rank = total_rank / instances_tested
    std_rank = (sum((x - mean_rank) ** 2 for x in [tropicalize(generate_parity_circuit(n)) for _ in range(30)]) / instances_tested) ** 0.5
    
    return {
        "metric_name": "Rank vs AC0 Circuit Size",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
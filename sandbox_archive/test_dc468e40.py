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
    
    def nisan_wigderson_prg(n, seed):
        prg = [random.randint(0, 1) for _ in range(n)]
        return prg
    
    def ac0_circuit(n):
        # Simulate a simple AC^0 circuit that outputs the XOR of all bits
        return sum(random.choice([0, 1]) for _ in range(n)) % 2
    
    def fool_ac0(prg, circuit):
        for i in range(len(prg)):
            if prg[i] != circuit(i):
                return False
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_tests = 0
    success_count = 0
    counterexample = ""
    
    for n in n_values:
        prg_length = int(math.log(n) * 2)  # Seed length to test
        if prg_length < 1:
            continue
        
        for _ in range(30):  # Test with 30 instances per seed
            prg = nisan_wigderson_prg(prg_length, seed)
            circuit_result = ac0_circuit(n)
            if not fool_ac0(prg, circuit_result):
                counterexample = f"n={n}, prg_length={prg_length}"
                break
        
        total_tests += 30
        success_count += 1
    
    metric_value = success_count / len(n_values)
    conjecture_holds = metric_value >= 0.8
    
    return {
        "metric_name": "success_rate",
        "metric_value": metric_value,
        "instances_tested": total_tests,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
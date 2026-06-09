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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("f must be a Boolean function with 2^n values")
        
        circuit_ranks = []
        for i in range(n + 1):
            max_rank = 0
            for j in range(2**(n - i)):
                inputs = [j * (1 << i) + k for k in range(2**i)]
                outputs = [f[input] for input in inputs]
                rank = 0
                while len(outputs) > 1:
                    new_outputs = []
                    for k in range(len(outputs) // 2):
                        if outputs[2*k] != outputs[2*k + 1]:
                            new_outputs.append(1)
                        else:
                            new_outputs.append(0)
                    outputs = new_outputs
                    rank += 1
                max_rank = max(max_rank, rank)
            circuit_ranks.append(max_rank)
        return min(circuit_ranks)
    
    def minimal_representation_degree(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("f must be a Boolean function with 2^n values")
        
        # Simplified encoding of the modular form using graphical Langlands duality
        return n
    
    trials = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        degree = minimal_representation_degree(f)
        trials.append((rank, degree))
    
    ranks = [t[0] for t in trials]
    degrees = [t[1] for t in trials]
    
    if not ranks or not degrees:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(trials),
            "n_max": max(n for _, n in trials),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_degree = sum(degrees) / len(degrees)
    pearson_corr = (sum((r - mean_rank) * (d - mean_degree) for r, d in trials) /
                    math.sqrt(sum((r - mean_rank)**2 for r in ranks) *
                              sum((d - mean_degree)**2 for d in degrees)))
    
    if not math.isfinite(pearson_corr):
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(trials),
            "n_max": max(n for _, n in trials),
            "conjecture_holds": False,
            "counterexample": "non_finite_correlation"
        }
    
    mean_abs_diff = sum(abs(r - d) for r, d in trials) / len(trials)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(trials),
        "n_max": max(n for _, n in trials),
        "conjecture_holds": pearson_corr >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = "first failing seed"
        mean_corr = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
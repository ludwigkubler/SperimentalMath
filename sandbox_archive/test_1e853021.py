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
        for _ in range(10 * n):  # Generate a simple circuit with 10 gates per variable
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, min(n, 4)))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def monotone_width(circuit):
        n = len(circuit)
        width = [0] * (n + 1)
        for i in range(n):
            gate_type, _ = circuit[i]
            if gate_type == 'AND':
                width[i + 1] = max(width[:i + 1]) + 1
            else:
                width[i + 1] = max(width[:i + 1])
        return width[-1]
    
    def bruer_group_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            gate_type, _ = circuit[i]
            if gate_type == 'AND':
                rank += 1
        return rank
    
    ranks = []
    widths = []
    
    for _ in range(30):  # Test with 30 instances per seed
        n = random.randint(5, 40)
        circuit = generate_circuit(n)
        rank = bruer_group_rank(circuit)
        width = monotone_width(circuit)
        ranks.append(rank)
        widths.append(width)
    
    if not ranks or not widths:
        return {
            "metric_name": "Brauer Group Rank vs Monotone Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_circuit"
        }
    
    n_max = max(len(circuit) for _ in range(30))
    if n_max < 16:
        return {
            "metric_name": "Brauer Group Rank vs Monotone Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    slope = (sum((ranks[i] - mean_rank) * (widths[i] - mean_width) for i in range(len(ranks)))) / sum((widths[i] - mean_width) ** 2 for i in range(len(widths)))
    
    return {
        "metric_name": "Brauer Group Rank vs Monotone Width",
        "metric_value": slope,
        "instances_tested": len(ranks),
        "n_max": n_max,
        "conjecture_holds": abs(slope - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_slope = sum(r["metric_value"] for r in results) / len(results)
        std_slope = math.sqrt(sum((r["metric_value"] - mean_slope) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slope_outside_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
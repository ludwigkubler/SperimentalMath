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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_weight(circuit):
        weight = 0
        for gate, inputs in circuit:
            if gate == 'AND':
                weight += sum(inputs)
            elif gate == 'OR':
                weight += len(inputs) - sum(inputs)
        return weight
    
    def frobenius_schur_indicator(gate, inputs):
        if gate == 'AND':
            return Fraction(sum(inputs), 2**len(inputs))
        elif gate == 'OR':
            return Fraction(len(inputs) - sum(inputs), 2**len(inputs))
    
    def min_order(FSInds):
        return min(FSInd for FSInd in FSInds if FSInd != 0)
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    weight = compute_weight(circuit)
    FSInds = [frobenius_schur_indicator(gate, inputs) for gate, inputs in circuit]
    min_order_FSInd = min_order(FSInds)
    
    return {
        "metric_name": "min_order_FSInd_vs_weight",
        "metric_value": min_order_FSInd * weight,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["metric_value"] < 0.5 for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"] and res["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
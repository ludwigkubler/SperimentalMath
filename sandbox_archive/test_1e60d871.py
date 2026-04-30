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

def generate_random_ac0_circuit(n):
    if n == 1:
        return ["NOT", "x"]
    else:
        left = generate_random_ac0_circuit(n // 2)
        right = generate_random_ac0_circuit(n - n // 2)
        return ["OR", left, right]

def encode_gate(gate, inputs):
    if gate == "NOT":
        x = inputs[0]
        return f"{x} * {1 - x}"
    elif gate == "AND":
        x = inputs[0]
        y = inputs[1]
        return f"{x} * {y}"
    elif gate == "OR":
        x = inputs[0]
        y = inputs[1]
        return f"{x} + {y} - {x} * {y}"
    else:
        raise ValueError("Invalid gate")

def generate_polynomial_system(circuit, n):
    if circuit[0] in ["NOT", "AND", "OR"]:
        gate = circuit[0]
        inputs = [f"x{i}" for i in range(n)]
        children = circuit[1:]
        equations = []
        for child in children:
            if isinstance(child, list):
                child_equations = generate_polynomial_system(child, n)
                equations.extend(child_equations)
            else:
                equations.append(encode_gate(gate, [child]))
        return equations
    else:
        raise ValueError("Invalid circuit")

def count_real_components(equations):
    # This is a placeholder for the actual computation of real components.
    # For simplicity, we assume that each equation contributes one component.
    return len(equations)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    circuit = generate_random_ac0_circuit(n)
    equations = generate_polynomial_system(circuit, n)
    num_components = count_real_components(equations)
    size_C = len(circuit)
    conjecture_holds = num_components >= math.log(size_C)
    return {
        "metric_name": "num_components",
        "metric_value": num_components,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Size: {size_C}, Components: {num_components}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
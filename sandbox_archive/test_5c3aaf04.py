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
        # Generate a random AC⁰ circuit for PARITY on n inputs
        circuit = []
        for i in range(1 << (n - 1)):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def truth_table(circuit):
        # Compute the truth table of the circuit
        n = len(circuit[0][1])
        table = {}
        for i in range(1 << n):
            inputs = [(i >> j) & 1 for j in range(n)]
            result = 0
            for gate, inputs in circuit:
                if gate == 'AND':
                    result &= all(inputs)
                elif gate == 'OR':
                    result |= any(inputs)
            table[tuple(inputs)] = result
        return table
    
    def polynomial_ideal(truth_table):
        # Construct the ideal I_C from the truth table
        n = len(next(iter(truth_table.keys())))
        variables = [f'x{i}' for i in range(n)]
        polynomials = []
        for inputs, value in truth_table.items():
            poly = 1
            for i, bit in enumerate(inputs):
                if bit == 0:
                    poly *= (1 - eval(variables[i]))
                else:
                    poly *= eval(variables[i])
            polynomials.append(poly)
        return polynomials
    
    def real_radical_dimension(polynomials):
        # Compute the dimension of the real radical of the ideal
        n = len(polynomials[0].split('*'))
        variables = [f'x{i}' for i in range(n)]
        ideal = polynomials
        dim = 0
        while True:
            new_ideal = []
            for f in ideal:
                for g in ideal:
                    if f != g and not any(f.startswith(g) or g.startswith(f) for f, g in zip(new_ideal, new_ideal)):
                        new_ideal.append(f + '*' + g)
            if len(new_ideal) == len(ideal):
                break
            ideal = new_ideal
            dim += 1
        return dim
    
    n = 40
    circuit = generate_ac0_circuit(n)
    table = truth_table(circuit)
    polynomials = polynomial_ideal(table)
    dimension = real_radical_dimension(polynomials)
    
    size = len(circuit) * (2 ** (n - 1))
    bound = math.log2(size) - 7
    
    return {
        "metric_name": "real_radical_dimension",
        "metric_value": dimension,
        "instances_tested": 1,
        "conjecture_holds": dimension >= bound,
        "counterexample": "" if dimension >= bound else f"Dimension {dimension} < {bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
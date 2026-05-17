# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_random_circuit(n, d, s):
    gates = []
    for _ in range(s):
        if len(gates) < 2:
            gate_type = random.choice(['AND', 'OR', 'NOT', 'XOR'])
        else:
            gate_type = random.choice(['AND', 'OR', 'NOT', 'XOR', 'INPUT'])
        if gate_type == 'INPUT':
            gate = {'type': 'INPUT', 'inputs': [], 'output': random.randint(0, 1)}
        else:
            num_inputs = 2 if gate_type in ['AND', 'OR', 'XOR'] else 1
            inputs = random.sample(range(len(gates)), num_inputs)
            gate = {'type': gate_type, 'inputs': inputs}
        gates.append(gate)
    return gates

def evaluate_circuit(circuit, inputs):
    values = []
    for gate in circuit:
        if gate['type'] == 'INPUT':
            values.append(gate['output'])
        elif gate['type'] == 'NOT':
            values.append(1 - values[gate['inputs'][0]])
        elif gate['type'] == 'AND':
            values.append(values[gate['inputs'][0]] & values[gate['inputs'][1]])
        elif gate['type'] == 'OR':
            values.append(values[gate['inputs'][0]] | values[gate['inputs'][1]])
        elif gate['type'] == 'XOR':
            values.append(values[gate['inputs'][0]] ^ values[gate['inputs'][1]])
    return values[-1]

def compute_supp(circuit):
    supp = []
    for gate in circuit:
        if gate['type'] == 'INPUT':
            supp.append({gate['output']})
        elif gate['type'] == 'NOT':
            supp.append(supp[gate['inputs'][0]])
        else:
            s = set()
            for i in gate['inputs']:
                s.update(supp[i])
            supp.append(s)
    return supp

def build_gate_conflict_graph(circuit, supp):
    graph = defaultdict(set)
    gates = [i for i, gate in enumerate(circuit) if gate['type'] != 'INPUT']
    for i, j in itertools.combinations(gates, 2):
        if supp[i] & supp[j]:
            graph[i].add(j)
            graph[j].add(i)
    return graph

def is_independent_set(graph, S):
    for u in S:
        for v in S:
            if u != v and v in graph[u]:
                return False
    return True

def compute_tau(graph):
    independent_sets = []
    gates = list(graph.keys())
    for k in range(1, len(gates) + 1):
        for S in itertools.combinations(gates, k):
            if is_independent_set(graph, S):
                independent_sets.append(S)
    tau = sum((-1) ** len(S) for S in independent_sets)
    return tau

def mod_q(n, q):
    return sum(1 for inputs in itertools.product([0, 1], repeat=n) if sum(inputs) % q == 0)

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    d_values = [2, 3, 4]
    s_values = [8, 12, 16, 20]
    q_values = [3, 5]
    epsilon = 0.25

    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for d in d_values:
            for s in s_values:
                for q in q_values:
                    circuit = generate_random_circuit(n, d, s)
                    supp = compute_supp(circuit)
                    graph = build_gate_conflict_graph(circuit, supp)
                    tau = compute_tau(graph)

                    mod_q_value = mod_q(n, q)
                    agreement = sum(1 for inputs in itertools.product([0, 1], repeat=n) if evaluate_circuit(circuit, inputs) == (sum(inputs) % q == 0))

                    if agreement >= (1 - epsilon) * (2 ** n):
                        predicted_bound = 2 ** (n / (10 * d ** 2)) - 1
                        if tau < predicted_bound:
                            conjecture_holds = False
                            counterexample = f"n={n}, d={d}, s={s}, q={q}, tau={tau}, predicted_bound={predicted_bound}"
                            break
                        metric_values.append(tau)
                        instances_tested += 1
                if not conjecture_holds:
                    break
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if instances_tested == 0:
        return {
            "metric_name": "tau",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": True,
            "counterexample": ""
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "tau",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    instances_tested = 0
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        instances_tested += result["instances_tested"]
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]
            break

    if instances_tested == 0:
        print("RESULT: INCONCLUSIVE reason=no_instances_tested")
    elif not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={seed}')
    else:
        mean_metric = sum(metric_values) / len(metric_values)
        std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(1 for x in metric_values if x >= 0) / len(metric_values)
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
import random
import math
import sys
import json

def GF2_poly_add(poly1, poly2):
    return [poly1[i] ^ poly2[i] for i in range(len(poly1))]

def GF2_poly_mul(poly1, poly2):
    result = [0] * (len(poly1) + len(poly2) - 1)
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            if poly1[i] and poly2[j]:
                result[i + j] ^= 1
    return result

def GF2_poly_gcd(poly1, poly2):
    while poly2:
        degree_poly1 = len(poly1) - 1
        degree_poly2 = len(poly2) - 1
        if degree_poly1 < degree_poly2:
            poly1, poly2 = poly2, poly1
            degree_poly1, degree_poly2 = degree_poly2, degree_poly1
        leading_coeff_quotient = poly1[degree_poly1] // poly2[degree_poly2]
        quotient = [0] * (degree_poly1 - degree_poly2)
        quotient[degree_poly1 - degree_poly2] = leading_coeff_quotient
        poly1 = GF2_poly_sub(poly1, GF2_poly_mul(quotient, poly2))
    return poly1

def GF2_poly_mod(dividend, divisor):
    while len(dividend) >= len(divisor):
        degree_dividend = len(dividend) - 1
        degree_divisor = len(divisor) - 1
        leading_coeff_quotient = dividend[degree_dividend] // divisor[degree_divisor]
        quotient = [0] * (degree_dividend - degree_divisor)
        quotient[degree_dividend - degree_divisor] = leading_coeff_quotient
        dividend = GF2_poly_sub(dividend, GF2_poly_mul(quotient, divisor))
    return dividend

def GF2_poly_sub(poly1, poly2):
    return [poly1[i] ^ poly2[i] for i in range(len(poly1))]

def Buchberger_algorithm(polynomials):
    S = []
    G = polynomials[:]
    for i in range(len(G)):
        for j in range(i + 1, len(G)):
            s = GF2_poly_gcd(G[i], G[j])
            if s:
                S.append(s)
    while S:
        s = S.pop()
        degree_s = len(s) - 1
        found = False
        for i in range(len(G)):
            degree_Gi = len(G[i]) - 1
            if degree_Gi > degree_s and G[i][degree_s]:
                g = GF2_poly_mod(G[i], s)
                if g:
                    S.append(g)
                    found = True
                    break
        if not found:
            G.append(s)
    return G

def random_CNF(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clause.extend([-v for v in clause])
        clauses.append(clause)
    return clauses

def CNF_to_polynomials(CNF):
    variables = set(abs(v) for v in sum(CNF, []))
    polynomials = [0] * (2 ** len(variables))
    for clause in CNF:
        monomial = 1
        for v in clause:
            if v > 0:
                bit_position = variables.index(v)
                monomial |= 1 << bit_position
            else:
                bit_position = variables.index(-v)
                monomial &= ~(1 << bit_position)
        polynomials[monomial] += 1
    return [poly for poly in polynomials if poly]

def Extended_Frege_proof_size(CNF):
    n = len(set(abs(v) for v in sum(CNF, [])))
    m = len(CNF)
    return (n + m) * math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    m = 2 * n
    CNF = random_CNF(n, m)
    polynomials = CNF_to_polynomials(CNF)
    generators = Buchberger_algorithm(polynomials)
    proof_size = Extended_Frege_proof_size(CNF)
    generator_count = len(generators)
    conjecture_holds = abs(generator_count - proof_size) / proof_size < 0.1
    counterexample = "" if conjecture_holds else f"n={n}, m={m}, generators={generator_count}, proof_size={proof_size}"
    return {
        "metric_name": "Generator Count vs Proof Size",
        "metric_value": generator_count,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
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
        counterexample_desc = f"n={results[0]['metric_value']}, m=2*n, generators={results[0]['counterexample']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")

risk_factors = {
        "mask": 50,
        "knife": 40,
        "criminal_record": 30,
}

def evaluate(data):
    score = 0

    for k, v in risk_factors.items():
        if k in data:
            score += v

    return score


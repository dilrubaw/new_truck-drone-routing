def adaptive_cooling(
    current_temperature,
    base_beta,
    no_improve_count,
    threshold=50,
    max_beta=0.9995
):
    if no_improve_count > threshold:
        dynamic_beta = min(max_beta, base_beta + (1 - base_beta) * 0.5)
    else:
        dynamic_beta = base_beta

    return current_temperature * dynamic_beta
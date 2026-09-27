def validate_features(features, required):
    missing = set(required) - set(features)
    if missing:
        raise ValueError(f"Missing required features: {', '.join(sorted(missing))}")
    return features

def jaccard_similarity_mod(a: set, b: set) -> float:
  if not a and not b:
    return 0.0

  if len(a) == 0 or len(b) == 0:
    return 0.0

  return len(a.intersection(b)) / min(len(a), len(b))


__all__ = ["jaccard_similarity_mod"]

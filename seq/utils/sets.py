def jaccard_similarity_mod(a: set, b: set) -> float:
  return len(a.intersection(b)) / min(len(a), len(b))


__all__ = ["jaccard_similarity_mod"]

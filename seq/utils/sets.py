def jaccard_similarity(a: set, b: set) -> float:
  return len(a.intersection(b)) / len(a.union(b))


__all__ = ["jaccard_similarity"]

from sequilt.utils.sets import jaccard_similarity_mod


def test_identical_sets():
  a = {1, 2, 3}
  b = {1, 2, 3}
  assert jaccard_similarity_mod(a, b) == 1.0


def test_disjoint_sets():
  a = {1, 2, 3}
  b = {4, 5, 6}
  assert jaccard_similarity_mod(a, b) == 0.0


def test_subset_sets():
  a = {1, 2, 3}
  b = {1, 2}
  assert jaccard_similarity_mod(a, b) == 1.0


def test_overlapping_sets():
  a = {1, 2, 3}
  b = {2, 3, 4}
  assert jaccard_similarity_mod(a, b) == 2 / 3


def test_empty_sets():
  a = set()
  b = set()
  assert jaccard_similarity_mod(a, b) == 0.0


def test_one_empty_set():
  a = {1, 2, 3}
  b = set()
  assert jaccard_similarity_mod(a, b) == 0.0

from tokenizers import Tokenizer

tokenizer: Tokenizer = Tokenizer.from_pretrained("Xenova/gpt-4")

__all__ = ["tokenizer"]

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeReviewModel:
    def __init__(self, use_cuda=False):
        self.device = "cuda" if use_cuda and torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

        # Loading CodeBERT (CodeBERT-base)
        # Using a sequence classification head (randomly initialized if not fine-tuned)
        try:
            self.codebert_name = "microsoft/codebert-base"
            self.tokenizer = AutoTokenizer.from_pretrained(self.codebert_name)
            # We use 2 labels: 0 -> Clean, 1 -> Buggy
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.codebert_name, num_labels=2
            ).to(self.device)
            logger.info("CodeBERT model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load CodeBERT: {e}")
            self.model = None

        # Loading DistilBERT for lighter tasks if needed (optional)
        try:
            self.distil_name = "distilbert-base-uncased"
            self.distil_tokenizer = AutoTokenizer.from_pretrained(self.distil_name)
            self.distil_model = AutoModelForSequenceClassification.from_pretrained(
                self.distil_name, num_labels=2
            ).to(self.device)
            logger.info("DistilBERT model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load DistilBERT: {e}")
            self.distil_model = None

    def predict_bug_probability(self, code_snippet: str):
        """
        Predicts if a code snippet has a bug using CodeBERT.
        Returns a probability of being buggy.
        """
        if not self.model:
            return 0.5 # Fallback

        inputs = self.tokenizer(
            code_snippet, return_tensors="pt", truncation=True, max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            # Class 1 is 'Buggy'
            bug_prob = probs[0][1].item()
        
        return bug_prob

    def analyze_with_distilbert(self, text_snippet: str):
        """
        Use DistilBERT for faster analysis (e.g. comment quality or style).
        """
        if not self.distil_model:
            return 0.5

        inputs = self.distil_tokenizer(
            text_snippet, return_tensors="pt", truncation=True, max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.distil_model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            return probs[0][1].item()

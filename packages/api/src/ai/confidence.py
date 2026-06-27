from src.ai.schemas import ConfidenceLevel, AIParserOutput

def get_overall_confidence(output: AIParserOutput) -> ConfidenceLevel:
    """
    Calculates overall confidence based on field confidences.
    Simple implementation: if any is LOW, overall is LOW.
    If all are HIGH, overall is HIGH. Otherwise MEDIUM.
    """
    confidences = []
    confidences.append(output.customer_name.confidence)
    confidences.append(output.segmentation.confidence)
    confidences.append(output.delivery_date.confidence)
    confidences.append(output.remarks.confidence)

    for item in output.items:
        confidences.append(item.material_code.confidence)
        confidences.append(item.quantity.confidence)
        confidences.append(item.unit.confidence)
        confidences.append(item.target_price.confidence)

    if any(c == ConfidenceLevel.LOW for c in confidences):
        return ConfidenceLevel.LOW
    if all(c == ConfidenceLevel.HIGH for c in confidences):
        return ConfidenceLevel.HIGH
    return ConfidenceLevel.MEDIUM

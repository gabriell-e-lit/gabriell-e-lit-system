"""
run_extractor.py (v12 — skeleton)

Това е входната точка на екстрактора.
Той:
- създава pipeline
- регистрира екстракторите
- стартира процеса

Тази версия е архитектурен скелет — без реална логика.
"""

from AI_Library.automation.extractors.v12.pipeline import ExtractorPipeline
from AI_Library.utils.logging import Logger


def run_extractor(input_dir: str, output_dir: str):
    """
    Стартира екстрактора.
    Реалната логика за регистриране на екстрактори ще бъде добавена във v12.1.
    """
    logger = Logger("run_extractor")

    logger.info("Стартиране на екстрактора (skeleton).")

    pipeline = ExtractorPipeline(
        input_dir=input_dir,
        output_dir=output_dir,
        logger=logger
    )

    # Тук по-късно ще регистрираме екстракторите:
    # pipeline.register_extractor(ExtractAuthors(...))
    # pipeline.register_extractor(ExtractBios(...))
    # pipeline.register_extractor(ExtractIssues(...))
    # pipeline.register_extractor(ExtractCollections(...))
    # pipeline.register_extractor(ExtractLinks(...))

    pipeline.run()

    logger.info("Екстракторът завърши (skeleton).")


if __name__ == "__main__":
    # Тук по-късно ще добавим реални пътища
    run_extractor(
        input_dir="INPUT_DIR_PLACEHOLDER",
        output_dir="OUTPUT_DIR_PLACEHOLDER"
    )


"""
Extractor Pipeline (v12 — skeleton)

Това е централният orchestrator на екстрактора.
Той управлява:
- зареждането на отделните екстрактори
- последователността на изпълнение
- логването
- входните и изходните директории

Тази версия е архитектурен скелет — без реална логика.
"""

from typing import Optional, List
from AI_Library.utils.logging import Logger


class ExtractorPipeline:
    """
    Централен orchestrator за екстрактора (skeleton).
    """

    def __init__(self, input_dir: str, output_dir: str, logger: Optional[Logger] = None):
        """
        :param input_dir: директория с HTML файлове или други входни данни
        :param output_dir: директория за JSON резултати
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.logger = logger or Logger("ExtractorPipeline")

        # Тук по-късно ще зареждаме отделните екстрактори
        self.extractors: List = []

    # ---------------------------------------------------------
    # 1) Регистрация на екстрактори (skeleton)
    # ---------------------------------------------------------
    def register_extractor(self, extractor):
        """
        Регистрира екстрактор в pipeline.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.extractors.append(extractor)
        self.logger.info(f"(skeleton) Регистриран екстрактор: {extractor.__class__.__name__}")

    # ---------------------------------------------------------
    # 2) Изпълнение на всички екстрактори (skeleton)
    # ---------------------------------------------------------
    def run(self):
        """
        Изпълнява всички регистрирани екстрактори.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("ExtractorPipeline (skeleton) — стартиране.")

        for extractor in self.extractors:
            self.logger.info(f"(skeleton) Стартиране на {extractor.__class__.__name__}")
            extractor.run()

        self.logger.info("ExtractorPipeline (skeleton) — завършено.")


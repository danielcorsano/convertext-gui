"""Background conversion threads."""

import threading
import logging
import time
from pathlib import Path
from convertext.core import ConversionEngine

logger = logging.getLogger(__name__)


class ConversionThread(threading.Thread):
    """Background thread for file conversion."""

    def __init__(self, engine, files, formats, output_dir, overwrite, keep_intermediate, callback):
        super().__init__(daemon=True)
        self.engine = engine
        self.files = files
        self.formats = formats
        self.output_dir = output_dir
        self.overwrite = overwrite
        self.keep_intermediate = keep_intermediate
        self.callback = callback
        self.results = []
        self.start_time = None

    def run(self):
        """Execute conversions."""
        total = len(self.files) * len(self.formats)
        completed = 0
        self.start_time = time.time()

        logger.info(f"Starting conversion: {len(self.files)} files, {len(self.formats)} formats")

        # Update config
        if self.output_dir:
            self.engine.config.override({'output': {'directory': str(self.output_dir)}})
            logger.debug(f"Output directory: {self.output_dir}")

        if self.overwrite:
            self.engine.config.override({'output': {'overwrite': True}})
            logger.debug("Overwrite enabled")

        if self.keep_intermediate:
            self.engine.config.override({'conversion': {'keep_intermediate': True}})
            logger.debug("Keep intermediate files enabled")

        for file in self.files:
            for fmt in self.formats:
                logger.info(f"Converting {file.name} to {fmt}")

                try:
                    # Convert
                    result = self.engine.convert(file, fmt)
                    self.results.append(result)

                    if result.success:
                        logger.info(f"✓ {file.name} → {result.target_path.name}")
                    else:
                        logger.error(f"✗ {file.name}: {result.error}")

                except Exception as e:
                    logger.exception(f"Conversion failed for {file.name} to {fmt}: {e}")
                    # Create a mock result for error tracking
                    from types import SimpleNamespace
                    result = SimpleNamespace(
                        success=False,
                        source_path=file,
                        target_path=None,
                        error=str(e)
                    )
                    self.results.append(result)

                # Update progress with ETA
                completed += 1
                progress = (completed / total) * 100

                # Calculate ETA
                elapsed = time.time() - self.start_time
                if completed > 0:
                    avg_time = elapsed / completed
                    remaining = total - completed
                    eta_seconds = int(avg_time * remaining)
                    if eta_seconds > 60:
                        eta = f"{eta_seconds // 60}m {eta_seconds % 60}s"
                    else:
                        eta = f"{eta_seconds}s"
                else:
                    eta = "calculating..."

                status = f"Converting... {int(progress)}% | ETA: {eta}"

                self.callback(progress, status, result)

        # Finish
        logger.info(f"Conversion complete: {sum(1 for r in self.results if r.success)}/{len(self.results)} successful")
        self.callback(100, "Conversion complete!", None)

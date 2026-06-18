import logging
from pathlib import Path
from string import Template

from defs import *

logger = logging.getLogger(__name__)

with open("Makefile.in", "r") as f:
    MAKEFILE_TEMPLATE = Template(f.read())


class Source:
    def __init__(self, name: str, dir: Path, source_path: Path = Path()):
        self.name = name
        self.dir = dir
        self.source_path = source_path
        source_dir = dir / source_path

        if (source_dir / PARSER_FILE).exists():
            logger.info(f"{name}: Found parser.c")
            self.srcs = [source_path / PARSER_FILE]
        else:
            logger.error(f"{name}: No parser.c found")
            return

        if (source_dir / SCANNER_FILE).exists():
            logger.info(f"{name}: Found scanner.c")
            self.srcs.append(source_path / SCANNER_FILE)
        else:
            logger.info(f"{name}: No scanner.c found")

        self.incs = []
        for inc_src in (source_dir / INC_PATH).rglob("*.h"):
            logger.info(f"{name}: Found {inc_src.relative_to(dir)}")
            self.incs.append(inc_src.relative_to(dir))

        for support_src in (source_dir / SRC_PATH).glob("*.c"):
            rel = support_src.relative_to(dir)
            if rel not in self.srcs:
                logger.info(f"{name}: Found {rel}")
                self.incs.append(rel)

        for inc_src in (dir / "common").rglob("*.h"):
            logger.info(f"{name}: Found {inc_src.relative_to(dir)}")
            self.incs.append(inc_src.relative_to(dir))

    def get_makefile(self) -> str:
        return MAKEFILE_TEMPLATE.substitute(
            CSTD=DEFAULT_CSTD,
            INC_PATH=self.source_path / INC_PATH,
            SRCS=" ".join(map(str, self.srcs)),
        )

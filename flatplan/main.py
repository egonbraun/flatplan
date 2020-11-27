import fire
from sys import exit, stdin, stdout
from typing import Optional
from .flattener import PlanFlattener
from .logging import setup_logger


DEFAULT_ENCODING = "utf-8"


def main(
    jsonplan: Optional[str] = "",
    output: Optional[str] = "",
    debug: Optional[bool] = False,
) -> None:
    logger = setup_logger("flatplan", debug)
    fp_in = stdin
    fp_out = stdout

    logger.debug("Flattening...")

    if jsonplan:
        logger.debug(f"Reading plan from {jsonplan}")
        fp_in = open(jsonplan, "r", encoding=DEFAULT_ENCODING)

    if output:
        logger.debug(f"Output will be saved to {output}")
        fp_out = open(output, "w+", encoding=DEFAULT_ENCODING)

    json_in = fp_in.read()
    flattener = PlanFlattener(json_in,  logger=logger)
    json_out = flattener.flatten()
    fp_out.write(f"{json_out}\n")
    fp_in.close()
    fp_out.close()

    logger.debug("Flattened!")

    exit(0)


fire.Fire(main)

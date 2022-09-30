import click
from loguru import logger

import stats
from settings import Settings

logger.add("logging.log")


@click.command()
@click.option("--task")
@click.option("-n", type=int)
def main(task: str, n: int) -> None:
    presets = Settings()
    logger.info(f"starting {task} with {n}")
    if task == "clt":
        stats.central_limit(presets, n)
    if task == "simpsons":
        stats.simulate_simpson(presets)
    if task == "beta":
        stats.beta_examples(presets)


if __name__ == "__main__":
    main()

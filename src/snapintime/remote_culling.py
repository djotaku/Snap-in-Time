from snapintime.utils import config  # type: ignore

from . import culling, log


def main():
    our_config = config.import_config()
    log.info(culling.cull_snapshots(our_config, True))


if __name__ == "__main__":  # pragma: no cover
    log.info("Beginning remote culling...")
    main()

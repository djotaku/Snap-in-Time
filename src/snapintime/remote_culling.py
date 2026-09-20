from snapintime.utils import config  # type: ignore

from . import StructuredMessage, culling, log, slog


def main():
    our_config = config.import_config()
    result = culling.cull_snapshots(our_config, True)
    log.info(result)
    slog.info(
        StructuredMessage("Culling", result=result)
    )  # may need to tweak things here to get something useful


if __name__ == "__main__":  # pragma: no cover
    log.info("Beginning remote culling...")
    main()

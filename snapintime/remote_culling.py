from snapintime.utils import config as config  # type: ignore

from . import culling, log


def main():
    our_config = config.import_config()
    # three day cull doesn't make sense because it's only 1 per day already (at least most days)
    weekly_cull_result = culling.cull_seven_days_ago(our_config, True)
    quarterly_cull_result = culling.cull_last_quarter(our_config, True)
    yearly_cull_result = culling.cull_last_year(our_config, True)
    log.info(weekly_cull_result)
    log.info(quarterly_cull_result)
    log.info(yearly_cull_result)


if __name__ == "__main__":  # pragma: no cover
    log.info("Beginning remote culling...")
    main()

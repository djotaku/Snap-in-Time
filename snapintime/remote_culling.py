from . import culling
from . import log
from snapintime.utils import config as config  # type: ignore


our_config = config.import_config()
# three day cull doesn't make sense because it's only 1 per day already (at least most days)
# weekly doesn't make sense either since that one is leaving 1 per day a week out
# quarterly is the first one that makes sense to implement.
quarterly_cull_result = culling.cull_last_quarter(our_config, True)
log.info(quarterly_cull_result)

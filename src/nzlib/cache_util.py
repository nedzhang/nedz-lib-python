from datetime import datetime, timedelta
import functools
import logging
# import util_logging

logger = logging.getLogger(__name__)

# import inspect

def timed_cache(**timedelta_kwargs):

    def _wrapper(f):
        update_delta = timedelta(**timedelta_kwargs)
        next_update = datetime.utcnow() + update_delta

        # print('f member: ', inspect.getmembers(f))

        logger.info('initiate cache for function %s. Next_update is %s with delta of %s',
                 f.__qualname__, next_update, update_delta)
        # Apply @lru_cache to f with no cache size limit
        f = functools.lru_cache(None)(f)

        @functools.wraps(f)
        def _wrapped(*args, **kwargs):
            nonlocal next_update
            now = datetime.utcnow()
            if now >= next_update:
                f.cache_clear()
                next_update = now + update_delta
                logger.info(
                    'cache expired. Set next_update is %s', next_update)
            return f(*args, **kwargs)
        return _wrapped
    return _wrapper

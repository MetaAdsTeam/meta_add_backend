import signal

import tornado.ioloop
import tornado.web

import root
import root.enums as enums
from root.handlers import *
from root.log_lib import get_logger

logger = get_logger('API')
loop = tornado.ioloop.IOLoop.current()


def all_handlers():
    return [
        tornado.web.url(fr"{root.context.uri_prefix}/adspots",
                        AdSpotsHandler, name=enums.UrlName.ADSPOTS.value),
        tornado.web.url(fr"{root.context.uri_prefix}/adspot/id/([0-9]+)/stream",
                        AdSpotStreamHandler, name=enums.UrlName.ADSPOT_STREAM.value),
        tornado.web.url(fr"{root.context.uri_prefix}/adspot/id/([0-9]+)",
                        AdSpotsHandler, name=enums.UrlName.ADSPOT_ID.value),
        tornado.web.url(fr"{root.context.uri_prefix}/adspot_stats/id/([0-9]+)",
                        AdSpotStatsIdHandler, name=enums.UrlName.ADSPOT_STATS_ID.value),
        tornado.web.url(fr"{root.context.uri_prefix}/adspot_types",
                        AdSpotTypesHandler, name=enums.UrlName.ADSPOT_TYPES.value),
        tornado.web.url(fr"{root.context.uri_prefix}/timeslots",
                        TimeSlotsHandler, name=enums.UrlName.TIMESLOTS.value),  # TODO: Remove
        tornado.web.url(fr"{root.context.uri_prefix}" + r"/timeslots/date/([0-9]{4}-[0-9]{2}-[0-9]{2})",
                        TimeSlotsDateHandler, name=enums.UrlName.TIMESLOTS_DATE.value),  # TODO: Remove
        tornado.web.url(fr"{root.context.uri_prefix}/timeslots_by_adspot/id/([0-9]+)",
                        TimeslotsByAdspotId, name=enums.UrlName.TIMESLOTS_BY_ADSPOT_ID.value),
        # tornado.web.url(fr"{root.context.uri_prefix}" +
        #                 r"/timeslots_by_adspot/id/([0-9]+)/date/([0-9]{4}-[0-9]{2}-[0-9]{2})",
        #                 TimeslotsByAdspotId, name=enums.UrlName.TIMESLOTS_BY_ADSPOT_ID_DATE.value),
        tornado.web.url(fr"{root.context.uri_prefix}/playbacks",
                        PlaybacksHandler, name=enums.UrlName.PLAYBACKS.value),
        tornado.web.url(fr"{root.context.uri_prefix}/playback",
                        PlaybacksHandler, name=enums.UrlName.PLAYBACK.value),
        tornado.web.url(fr"{root.context.uri_prefix}/playback/id/([0-9]+)",
                        PlaybacksHandler, name=enums.UrlName.PLAYBACK_ID.value),
        tornado.web.url(fr"{root.context.uri_prefix}/creatives",
                        CreativesHandler, name=enums.UrlName.CREATIVES.value),
        tornado.web.url(fr"{root.context.uri_prefix}/creative",
                        CreativesHandler, name=enums.UrlName.CREATIVE.value),
        tornado.web.url(fr"{root.context.uri_prefix}/creative/id/([0-9]+)",
                        CreativesHandler, name=enums.UrlName.CREATIVE_ID.value),
    ]


def stop():
    logger.info('Stopping application...')
    root.context.stop()
    loop.stop()
    logger.info('Stopped.')


def make_app():
    app_settings = {
        'static_path': root.context.static_path,
        # 'template_path': root.context.templates_path,
        # 'cookie_secret': root.context.api_secret,
        'debug': root.context.debug_mode,
        # 'login_url': "/login",
    }
    return tornado.web.Application(all_handlers(), **app_settings)


def log_function(handler):
    if handler.get_status() < 400:
        log_method = logger.info
    elif handler.get_status() < 500:
        log_method = logger.warning
    else:
        log_method = logger.error
    request_time = 1000.0 * handler.request.request_time()
    log_method(
        "%d %s %.2fms",
        handler.get_status(),
        handler._request_summary(),
        request_time,
    )


def start(port: int = 5000):
    app = make_app()
    app.listen(port)

    root.context.load_db_controller()

    app.settings.update({
        # 'executor': root.context.executor,
        'log_function': log_function,
        'context': root.context,
        'logger': logger,
    })

    # Base SIG handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(
            sig,
            lambda signum, stack: tornado.ioloop.IOLoop.current().add_callback_from_signal(stop)
        )

    logger.info('Starting Application')
    loop.start()

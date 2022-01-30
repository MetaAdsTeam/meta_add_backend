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
        tornado.web.url(fr"{root.context.uri_prefix}/", MainHandler, name=enums.UrlName.MAIN.value),
        tornado.web.url(fr"{root.context.uri_prefix}/ad_places", AdPlaces, name=enums.UrlName.ADPLACES.value),
        tornado.web.url(fr"{root.context.uri_prefix}/adspot_type", AdSpotType, name=enums.UrlName.ADSPOT_TYPE.value),
        tornado.web.url(fr"{root.context.uri_prefix}/adspot", AdSpot, name=enums.UrlName.ADSPOT.value),
        tornado.web.url(fr"{root.context.uri_prefix}/adspot/id/([0-9]+)", AdSpotId, name=enums.UrlName.ADSPOT_ID.value),
        tornado.web.url(fr"{root.context.uri_prefix}/timeslot", TimeSlot, name=enums.UrlName.TIMESLOT.value),
        tornado.web.url(fr"{root.context.uri_prefix}/timeslot/id/([0-9]+)", TimeSlotId, name=enums.UrlName.TIMESLOT_ID.value),
        tornado.web.url(fr"{root.context.uri_prefix}/playback", Playback, name=enums.UrlName.PLAYBACK.value),
        tornado.web.url(fr"{root.context.uri_prefix}/playback_status", PlaybackStatus, name=enums.UrlName.PLAYBACK_STATUS.value),
        tornado.web.url(fr"{root.context.uri_prefix}/content", Content, name=enums.UrlName.CONTENT.value),
        tornado.web.url(fr"{root.context.uri_prefix}/content_type", ContentType, name=enums.UrlName.CONTENT_TYPE.value),
        tornado.web.url(fr"{root.context.uri_prefix}/publisher", Publisher, name=enums.UrlName.PUBLISHER.value),
        tornado.web.url(fr"{root.context.uri_prefix}/advertiser", Advertiser, name=enums.UrlName.ADVERTISER.value),
    ]


def stop():
    logger.info('Stopping application...')
    root.context.stop()
    loop.stop()
    logger.info('Stopped.')


def make_app():
    app_settings = {
        # 'static_path': root.context.static_path,
        # 'template_path': root.context.templates_path,
        # 'cookie_secret': root.context.api_secret,
        # 'debug': root.context.debug_mode,
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
    })

    # Base SIG handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(
            sig,
            lambda signum, stack: tornado.ioloop.IOLoop.current().add_callback_from_signal(stop)
        )

    logger.info('Starting Application')
    loop.start()

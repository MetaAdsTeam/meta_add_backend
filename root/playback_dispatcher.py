import signal
import time
from threading import Thread

import requests

import root


class PlaybackDispatcher:
    def __init__(self):
        self.alive = False
        self.__loop_thread = Thread(
            target=self.component_loop,
            name='PlaybackDispatcherLoop'
        )
        self.__logger = None

    @property
    def logger(self) -> 'root.log_lib.Logger':
        if self.__logger is None:
            self.__logger = root.log_lib.get_logger(self.__class__.__name__)
        return self.__logger

    def start(self):
        self.alive = True
        self.add_signals()
        self.__loop_thread.start()

    def serve(self):
        while self.alive:
            time.sleep(1)

    def add_signals(self):
        # Base SIG handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, lambda _, __: self.stop())

    def stop(self):
        self.alive = False
        self.__loop_thread.join()

    def component_loop(self):
        while self.alive:
            self.component_iteration()
            time.sleep(1)

    def component_iteration(self):
        with root.context.sc as sc:
            ms = root.MS(sc.session)
            ad_tasks = ms.allocate_pending_playbacks()
            if ad_tasks:
                self.logger.info(f'Fetched {len(ad_tasks)} ad tasks')
                for ad_task in ad_tasks:
                    self.send_ad_task(ad_task)
                    ms.mark_playback_processed(ad_task.playback_id)

    def send_ad_task(self, ad_task: 'root.dc.AdTask'):
        r: 'requests.Response' = requests.post(
            ad_task.api_url,
            json=ad_task.config.__dict__
        )
        if r.status_code < 400:
            self.logger.info(
                f'Playback {ad_task.playback_id} was sent to {ad_task.api_url}.'
                f'File: {ad_task.config.name}'
            )
        else:
            self.logger.warning(
                f'Failed to sent task to {ad_task.api_url}. '
                f'Status: {r.status_code}. Response: {r.content}'
            )

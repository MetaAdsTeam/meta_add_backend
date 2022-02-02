from root import PlaybackDispatcher


if __name__ == "__main__":
    dispatcher = PlaybackDispatcher()
    dispatcher.start()
    dispatcher.serve()

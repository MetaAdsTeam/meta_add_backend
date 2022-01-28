from argparse import ArgumentParser

import root.app as app


def parse_arguments() -> int:
    parser = ArgumentParser(description='Tornado web-server')
    parser.add_argument('--port', '-p', help='listen on port', type=int, default=5000)
    args = parser.parse_args()
    return args.port


if __name__ == "__main__":
    port = parse_arguments()
    app.start(port)

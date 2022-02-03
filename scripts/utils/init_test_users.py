from root import context
from root.models import Advertiser


if __name__ == '__main__':
    with context.sc as sc:
        sc.session.add(Advertiser('admin', 'admin', 'Admin', 'https://admin.ref/'))
        sc.session.add(Advertiser('roman', 'roman', 'Roman', 'https://roman.ref/'))

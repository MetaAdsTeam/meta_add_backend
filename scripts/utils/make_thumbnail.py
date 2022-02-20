import root
import root.models as models
import root.utils as utils


def regenerate_creative_thumbnails():
    with root.context.sc as sc:
        creatives = sc.session.query(
            models.Creative
        ).filter(
            models.Creative.thumbnail.is_(None)
        ).all()
        for i, creative in enumerate(creatives, start=1):
            print(f'Processing {i}/{len(creatives)}')
            thumbnail = utils.make_thumbnail(creative.path)
            creative.thumbnail = thumbnail


if __name__ == '__main__':
    utils.make_thumbnail('C:\\Users\\Alexander\\Downloads\\Earth.mp4')
    # regenerate_creative_thumbnails()

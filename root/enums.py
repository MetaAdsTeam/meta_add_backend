from enum import Enum, IntEnum


class UrlName(Enum):
    """
    Project URLs names
    """
    LOGIN = "login"
    MAIN = "main"
    ADPLACES = 'adplaces'
    ADSPOT_TYPES = 'adspot_types'
    ADSPOTS = 'adspots'
    ADSPOT_ID = 'adspot_id'
    ADSPOT_STATS_ID = 'adspot_stats_id'
    TIMESLOTS = 'timeslots'
    TIMESLOTS_DATE = 'timeslots_date'
    TIMESLOT_ID = 'timeslot_id'
    PLAYBACKS = 'playbacks'
    PLAYBACK_ID = 'playback_id'
    PLAYBACK = 'playback'
    PLAYBACK_STATUS = 'playback_status'
    CREATIVES = 'creatives'
    CREATIVE = 'creative'
    CREATIVE_ID = 'creative_id'
    CREATIVE_TYPES = 'creative_types'
    PUBLISHER = 'publisher'
    ADVERTISER = 'advertiser'
    TIMESLOTS_BY_ADSPOT_ID = 'timeslots_by_adspot_id'

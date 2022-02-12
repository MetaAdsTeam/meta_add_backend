from enum import Enum, IntEnum


class UrlName(Enum):
    """
    Project URLs names
    """
    LOGIN = "login"
    ADSPOT_TYPES = 'adspot_types'
    ADSPOTS = 'adspots'
    ADSPOT_ID = 'adspot_id'
    ADSPOT_STREAM = 'adspot_stream'
    ADSPOT_STATS_ID = 'adspot_stats_id'
    TIMESLOTS = 'timeslots'
    TIMESLOTS_DATE = 'timeslots_date'
    PLAYBACKS = 'playbacks'
    PLAYBACK_ID = 'playback_id'
    PLAYBACK = 'playback'
    CREATIVES = 'creatives'
    CREATIVE = 'creative'
    CREATIVE_ID = 'creative_id'
    CREATIVE_ID_REF = 'creative_id_ref'
    TIMESLOTS_BY_ADSPOT_ID = 'timeslots_by_adspot_id'
    TIMESLOTS_BY_ADSPOT_ID_DATE = 'timeslots_by_adspot_id_date'


class PlaybackStatus(Enum):
    preparing = 'preparing'
    signed = 'signed'
    minting = 'minting'
    minted = 'minted'
    performing = 'performing'
    success = 'success'

"""Constants for the Garmin Scale Sync integration."""

DOMAIN = "garmin_scale_sync"


# defining entities suffixes
SUFFIX_WEIGHT = "gsc_body_weight"
SUFFIX_BODYFAT = "gsc_body_fat"
SUFFIX_MUSCLEWEIGHT = "gsc_muscle_weight"
SUFFIX_VICERALFAT = "gsc_viceralfat"
SUFFIX_MEASUREMENT_DATETIME = "gsc_measurementDateTime"
SUFFIX_BTN_SEND_DATA = "gsc_btnSendtoConnect"

# defining Config Keys
GSC_MUSCLEDATA_UNITS = "muscleDataDefinedUnit"
GSC_OAUTH_TOKEN = "oauthToken"
GSC_BODY_HEIGHT = "bodyheight"

# defining some enums
GARTH_LOGIN_SUCCESS = 1
GARTH_LOGIN_FAILED = 0


# defining keys for the user in which unit they wil type in the
# musclemass
MUSCLEMASS_INPUT_UNIT = ["kg", "%"]

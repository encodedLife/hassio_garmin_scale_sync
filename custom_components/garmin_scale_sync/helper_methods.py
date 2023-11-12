# Future imports for compatibility with both Python 2 and 3. Safe to remove if Python 3.3+ only.
from __future__ import annotations

# Imports for handling configuration entries and for platform constants.
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

# Import for handling time and date.
from homeassistant.util import dt as dt_util

# Import custom constants specific to this integration.
from .const import (
    DOMAIN,  # A constant for the integration domain.
    SUFFIX_WEIGHT,  # Constants for various measurement suffixes used to identify unique sensor data.
    SUFFIX_BODYFAT,
    SUFFIX_MUSCLEWEIGHT,
    SUFFIX_VICERALFAT,
    SUFFIX_MEASUREMENT_DATETIME,
    GSC_OAUTH_TOKEN,
    GSC_BODY_HEIGHT,
    GSC_MUSCLEDATA_UNITS,
)

# Imports for constructing and manipulating FIT files.
from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.weight_scale_message import WeightScaleMessage
from fit_tool.profile.profile_type import (
    Manufacturer,
    FileType,
)

# Standard library imports for handling time and date.
import time
import datetime

# Import Home Assistant's entity registry helper for working with entities.
from homeassistant.helpers import entity_registry as er

# Import BytesIO for handling binary data in memory.
from io import BytesIO

import garth

####################################################################################################
## Functions for the button
####################################################################################################


async def async_send_values_to_garmin(
    unique_id: str, hassHandler: HomeAssistant
) -> bool:
    """
    Sends weight, body fat, muscle weight, visceral fat, and measurement date to Garmin Connect
    using the provided unique_id and HomeAssistant instance.

    Args:
        unique_id (str): The unique ID of the Garmin Connect account to send the data to.
        hassHandler (HomeAssistant): The HomeAssistant instance to use for retrieving the data.

    Returns:
        bool: True if the data was successfully sent, False otherwise.
    """
    # getting the oauth token from the config entry
    token_garth = hassHandler.config_entries.async_get_entry(unique_id).data[
        GSC_OAUTH_TOKEN
    ]

    bodyheight = hassHandler.config_entries.async_get_entry(unique_id).data[
        GSC_BODY_HEIGHT
    ]

    muscleWeightUnit = hassHandler.config_entries.async_get_entry(unique_id).data[
        GSC_MUSCLEDATA_UNITS
    ]

    # getting the data from the number entities
    bodyweight = await get_state_by_unique_id(
        hassHandler, f"{unique_id}_{SUFFIX_WEIGHT}", Platform.NUMBER
    )
    bodyfat = await get_state_by_unique_id(
        hassHandler, f"{unique_id}_{SUFFIX_BODYFAT}", Platform.NUMBER
    )
    musclew = await get_state_by_unique_id(
        hassHandler, f"{unique_id}_{SUFFIX_MUSCLEWEIGHT}", Platform.NUMBER
    )
    viceral = await get_state_by_unique_id(
        hassHandler, f"{unique_id}_{SUFFIX_VICERALFAT}", Platform.NUMBER
    )
    measurement_date = await get_state_by_unique_id(
        hassHandler, f"{unique_id}_{SUFFIX_MEASUREMENT_DATETIME}", Platform.DATETIME
    )

    # converting the datetime to a timestamp nanoseconds
    measuTS = datetime_to_timestamp(measurement_date)

    # converting the values to the correct type
    bodyweight = float(bodyweight)
    bodyfat = float(bodyfat)
    musclew = float(musclew)

    # converting the muscleweight to kg
    # if it is in percent
    if muscleWeightUnit == "%":
        # muscleToExport= (musclem[percent]* bodyweight[kg])/100
        musclew = (musclew * bodyweight) / 100

    # calculating bmi
    bmi = bodyweight / ((bodyheight / 100) ** 2)

    # converting the viceral fat to an int
    viceral = int(float(viceral))

    fit_Data = create_FIT_FileStructure(
        body_weight=bodyweight,
        body_fat_percent=bodyfat,
        muscle_mass=musclew,
        visceral_fat_rating=viceral,
        bmi_val=bmi,
        timestamp_measurement=measuTS,
    )

    # Create a file-like object from the FIT file data
    binaryData = BytesIO(fit_Data.to_bytes())
    # Set the name of the file-like object
    binaryData.name = "weight.fit"

    # Upload the file-like object using garth.client.upload() method
    # garth.client.loads() method is used to load the oauth token
    garth.client.loads(token_garth)
    uploaded = await hassHandler.async_add_executor_job(garth.client.upload, binaryData)

    return True


async def get_state_by_unique_id(
    hass: HomeAssistant, unique_id: str, platform: str
) -> any | None:
    """Return the state of an entity by its unique ID."""

    # Get the entity registry
    entity_reg = er.async_get(hass)

    # Get the entity entry from the registry
    entity_entry = entity_reg.async_get_entity_id(platform, DOMAIN, unique_id)

    # check if the entity exists
    if entity_entry:
        # Get the state of the entity with the given entity_ID
        state = hass.states.get(entity_entry)
        return state.state if state else None
    return None


def datetime_to_timestamp(enity_state: str) -> int:
    """
    Converts a datetime string in the format "YYYY-MM-DD HH:MM:SS" to a Unix timestamp.

    Parameters:
    - datetime_str (str): The datetime string to convert.

    Returns:
    - int: The Unix timestamp corresponding to the given datetime.
    """
    date_obj = dt_util.parse_datetime(enity_state)
    # convert to Unix timestamp
    timestamp = int(time.mktime(date_obj.timetuple()))
    # multiply by 1000 to get milliseconds
    return timestamp * 1000


def create_FIT_Header(
    Type: FileType, manufacturer: Manufacturer, product_Num=0, serial_number=0x47111174
):
    """
    Creates a FIT file header based on the given parameters.
    """
    file_id_message = FileIdMessage()
    file_id_message.type = Type
    file_id_message.manufacturer = manufacturer
    file_id_message.product = product_Num
    file_id_message.time_created = round((datetime.datetime.now().timestamp() * 1000))
    file_id_message.serial_number = serial_number

    return file_id_message


def create_FIT_FileStructure(
    body_weight: float,
    body_fat_percent: float,
    muscle_mass: float,
    visceral_fat_rating: int,
    bmi_val: float,
    timestamp_measurement: int,
):
    """
    Creates a FIT file structure based on the given parameters.
    """
    fit_header = create_FIT_Header(
        Type=FileType.WEIGHT, manufacturer=Manufacturer.DEVELOPMENT
    )

    weightToExport = WeightScaleMessage()
    weightToExport.timestamp = timestamp_measurement
    weightToExport.visceral_fat_rating = visceral_fat_rating
    weightToExport.weight = body_weight
    weightToExport.percent_fat = body_fat_percent
    weightToExport.muscle_mass = muscle_mass
    weightToExport.bmi = bmi_val

    builder = FitFileBuilder(auto_define=True, min_string_size=50)
    builder.add(fit_header)
    builder.add(weightToExport)
    fit_file = builder.build()

    return fit_file

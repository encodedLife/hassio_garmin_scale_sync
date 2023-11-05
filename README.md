# Garmin Scale Sync Integration for Home Assistant

## Known Issues

Currently, the Garmin Connect integration is a work in progress and is classified as "In Development." Please be aware that, given its early stage, the integration might contain some bugs that have not yet been identified. I have not conducted extensive user testing, but I'm actively working on detecting and fixing any issues within the codebase.

I am dedicated to enhancing this integration and will roll out updates as fixes and improvements are implemented. Should you encounter any problems, I encourage you to report them. Your feedback is crucial for identifying and addressing issues promptly and will be incredibly helpful in prioritizing fixes in the development queue.

I appreciate your patience and any contributions you might make during this developmental phase. Detailed reports on any known issues that persist after initial testing will be provided, along with their current status and the approach being taken to resolve them.

Thank you for your support and stay tuned for continuous improvements.


## Overview
The Garmin Scale Sync integration allows Home Assistant to interact with your Garmin account, enabling the synchronization of various health metrics such as body weight, body fat percentage, muscle mass, and visceral fat. This integration aims to bridge your health data from your home environment into the Garmin ecosystem for a comprehensive health and activity tracking.

## Features
- **Data Sync**: Automatically sends scale measurements from Home Assistant to Garmin Connect.
- **Health Metrics**: Supports syncing multiple health metrics, including body weight, body fat percentage, muscle mass, and visceral fat rating.
- **Timestamp Synchronization**: Ensures that the time of the measurement is accurately reflected in the Garmin Connect data.

## Installation



## Configuration
Configuration is performed through the Home Assistant UI. Once authenticated, you can select which metrics to sync and configure the frequency of synchronization.

## Usage
After setup, the integration will listen for changes to the specified entities representing the health metrics. When a change is detected, or at the configured interval, the integration will automatically send an update to Garmin Connect.

## Code Structure
The codebase is structured as follows:
Entities:
button.py
number.py
datetime.py

## Dependencies
- `garth`: An amazing Python library to interface with Garmin Connect API and MFA. Developed by [matin](https://github.com/matin)
- `fit_tool`: A very useful utility library for creating FIT files compatible with Garmin's requirements. Developed by [mtucker](https://pypi.org/user/mtucker)

## Contributing
Contributions to the Garmin Scale Sync integration are welcome! Please submit pull requests with any enhancements, bug fixes, or improvements you wish to share.

## Support
For support and discussions, please open an issue on the GitHub repository.




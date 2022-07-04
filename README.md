# cutometer

## What is this?

The rotational speed and the edge alignment of the blade are important
factors affecting a sword cut. They are difficult to measure outside of
actual cutting situations involving physical targets such as tatami mats
which makes it hard to practice. Traditional techniques involve things
like listening to the whistling sound a thicker sword makes or an
instructor observing from outside and trying to see your movement.

This project aims to measure these parameters using the motion tracking
technology. It further aims to be robust and convenient enough to be used
in sparring situations.

## How it works?

A small motion tracking device is installed on the hilt. Since a sword is
a rigid body, both the rotational speed of the tip and any changes in the
edge alignment can be measured from that location.

Implementation uses MetaWear sensors from [MBientLab](https://mbientlab.com)
which have built-in sensor fusion capability, bluetooth connection, a decent
SDK and a good price point. Development is done with the MetamotionS model
which has nice plastic case.

## Installation

You need Python3 with PySide6, pyquaternion and MetaWear Python SDK installed.

## Usage

cutometer.py <macaddrofsensor>

You can get the mac addr from "hcitool lescan" (on Linux) output or a similar
command on your operating system.

## ToDo

This project is very crude at the moment. Configuration in particular is
entirely missing and requires code changes.

Edge alignment detection only tracks relative changes during the movement.
Alignment between cut path and the edge is not calculated.

Recording of the data is missing too.

## License

Cutomer is licensed under GNU GPL v3 or later.

#!/usr/bin/env bash

echo "configuring pins"
config-pin P9_14 pwm
config-pin P9_16 pwm
config-pin P9_22 pwm
config-pin P9_21 pwm

echo "read back"
config-pin -q P9_14
config-pin -q P9_16
config-pin -q P9_22
config-pin -q P9_21



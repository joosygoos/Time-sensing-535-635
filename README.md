# Time-sensing-535-635

## Team Members
1. Panashe Mandebvu
2. Jenny Yang
3. Joshua Gu

## Introduction

## Design Goals
Our goal is to replicate the time syncing system modeled in HAEST. This refers to a scalable, cost efficient, universal time synchronization system that solves the inherent latencies and shortcomings of current time-syncing protocols. 

This system utilizes multiple sensing modalities (of the same type) attached to two low power microcontrollers (ESP-32s). The two low power devices (IoT devices) are responsible for timestamping sensed ambient events. These events are sent to a gateway device (Raspberry Pi) which is responsible for computing the time-sync of the IoT devices. The gateway correlates the timestamps of the event across the sensors in order to calculate clock offset and frequency drift between the two IoT devices. In order to minimize power consumption in time syncing, the IoT devices will utilize ESP-E2’s bluetooth module to stream data to the gateway device. 

This approach to time synchronization allows for the addition of new sensing modalities into the same distributed system while minimizing calibration cost.

## Deliverables

## System Design
The following diagram shows our setup for calculating clock offsets from 2 ESP32's using a Raspberry Pi acting as the gateway device. The main role for the ESP32's is to collect and forward sensor data using 2 audio sensors on each ESP32. We will play some sound on a phone (like a door slamming) to simulate ambient sounds for the sensors. The Raspberry Pi collects the timestamped sensor data and calculates the clock drift of the devices. Following the HAEST paper (under [References](./README.md#References)), we predict to use a similar algorithm for identifying when 2 ESP32's detect the same event (sound from phone) using event detection and event matching algorithms.
![Figure 1](./images/figures/Figure_1.png)

## Hardware/Software Requirements

## Team Roles

## Project Timeline
We have a rough estimate of tasks to do as well as when they should be done. While we don't have exact dates, we have estimates based on the month. The bullet points for each month are in order of which should be done first, though some tasks can be done at the same time independently:

* October
  * Read up on specifications of ESP32 and Raspberry Pi, search for helpful third party software/frameworks
  * Have code for ESP32 to collect timestamped data from audio sensors, verify sound is detected properly at the correct timestamp
  * Be able to send data from ESP32 to Raspberry Pi through some protocol, verify Raspberry Pi receives correct data
  * Collect various data for sound events using phone as audio source
  * OPTIONAL: If have time, begin work on event detection, have code to detect an event on a single ESP32
* November
  * Have code to match an event on an ESP32 to the correct event on a second ESP32 (**hard**)
  * Have code to calculate clock drift when given 2 matching events
  * Verify that clock drift calculations are accurate
  * Begin research report
* December (2 weeks at most)
  * Finish research report
  * Presentations

## References
1. HAEST: Harvesting Ambient Events to Synchronize Time across Heterogeneous IoT Devices

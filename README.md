# Time-sensing-535-635

## Team Members
1. Panashe Mandebvu
2. Jenny Yang
3. Joshua Gu

## Introduction

## Design Goals

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

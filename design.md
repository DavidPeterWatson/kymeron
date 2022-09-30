# 3D Printer Design

The purpose of this document is to provide details for design decision sand references

## General Design

Crossed Gantry

## Chamber
Fully enclosed and insulated chamber.
Possible clear to provide visibility of operation to increase ability to fix. Visible feedback.
Vacume holes at the base of chamber to suck of cnc debris.
Chamber is heated from vents placed around the based of the vertical side panels. The heat should rise and heat the bed as well as the air on the chamber.
The temperature of 3D printed polymers needs to be kept just below the Glass transition temprature to increase the 


## Gantry
Crossed Gantry
Each toolhead has its own roller. Only 1 degree of movement requires engaging.
2 motors for each axis increases force applied to each axis.
Nema 23 motors for higher forces
BTT Octopus pro with TMC5160 Pro so that Voltage can be increased to 48V for higher speeds and higher amps.

The actuators that drive the gantry beams are also the frame for the machine.
THe gantry only moves in the x and z directions, while the bed moves in the y direction.



## Bed
Bed is heated indirectly by heaters at the base of the printer. This has the affect of heating the entire insulated chamber.
Bed needs to be changable. Bed Types:
- Glass for 3d Printing
- Aluminium Slats with Hardboard for cnc
- Cutting board for vinyl cutter

The bed moves up and down (Y direction) starting at the top and moving down for 3D printing toolheads.
The bed is kinematically coupled to 2 of the vertical actuators and the center of a beam in a triangular formation. The beam is connected between the other 2 vertical actuators. All 4 vertical actuators provide the vertical frame supports for the machine.


## ToolHeads

List of toolheads:
- PLA Filament toolhead colour 1
- PLA Filament toolhead colour 2
- PVA Filament toolhead
- ABS Filament toolhead
- TPU Filament toolhead
- Bed Level sensor toolhead
- Camera toolhead
- 3D Scanner toolhead
- Vinyl Cutter toolhead
- CNC toolhead (with vacuum brush head)
  - Connects to x and z gantries to provide extra stability.
  - Attaches to gantries from the corner
- Laser Cutter toolhead
- Inkjet toolhead
- Clay printer toolhead
- Electrical Component placement (Robotic arm) toolhead
- Electrical wire printer toolhead
- Electrical Soldering toolhead

Toolheads will be built on CANBUS boards
https://biqu.equipment/products/bigtreetech-ebb-36-42-can-bus-for-connecting-klipper-expansion-device?variant=39760665182306
This allows for many toolheads to be connected to a single CANBUS through BTT Octopus pro canbus bridge.
toolhead changer does not need to change electronic connections.

Filament toolheads


## Sensors and attachments

### Smoke Detection Sensor
This provides feedback for possible fire so that the printer can be turned off and an alarm raised.

### Toolhead level sensor
A contact sensor provides micron accuracy of toolhead height for all toolheads. This allows the bed level sensor to be calibrated with all other sensors using the highest accuracy contact sensor. This accuracy is independant of bed type because all sensing is done with contact sensors.

### Filamnet toolhead cleaner
Separate component to the side for cleaning toolheads

### Cameras
Take video and photographs for machining


# Kymeron Design

The purpose of this document is to provide details for design decisions and references for Kymeron

## General Design

Kymeron is based on a crossed gantry 3d printer design. Different tools are loaded and unloaded by moving the carriage off the gantry rather than attaching a tool to the carriage.

## Name
The name "Kymeron" hints at the mythical Chimera which is a combination of many creatures. This maker machine is combination of many machines. The "-ron" suffix is inspired by the "Voron" project.


## Chamber
Fully enclosed and insulated chamber.
Possibly clear to provide visibility of operation to increase ability to fix. Visible feedback.
Vacuum holes at the base of chamber to suck out cnc debris.
Suck air in the bottom of the chamber and introduce hot air near the top.
The temperature of chamber and 3D printed polymers needs to be kept just below the glass transition temperature to increase the bonding.
https://3dsolved.com/3d-filament-glass-transition-temperatures/


## Frame
The actuators that drive the gantry beams are also the frame for the machine.
The gantry only moves in the x and y directions, while the bed moves in the z direction.

2 motors for each horizontal axis increases force applied to each axis.
Nema 23 motors for higher forces
BTT Octopus pro with TMC5160 Pro so that Voltage can be increased to 48V for higher speeds and higher amps.



4 x z-axis linear actuators to move the bed vertically.
Vertical linear actuators also form the vertical frame.
Vertical linear actuators are C-Beam extrusions with stepper motors mounted at the top.
z-axis front left
z-axis back left
z-axis back right
z-axis front right

The x axis (left to right motion) is controlled by 2 linear actuators. One across the front and the other across the back.
x-axis front
x-axis back
The x-axis beam spans from the front x-axis cart to the back x-axis cart.
The x-axis beam sits under the y-axis and caries the tool carriages. 

The y axis (front to back motion) is controlled by 2 linear actuators. One across the left and the other across the right.
y-axis left
y-axis right
The y-axis beam spans from the left y-axis cart to the right y-axis cart.


## Gantry
Crossed Gantry
Each tool has its own carriage. Only 1 degree of movement requires engaging.
A special carriage made from a cbeam gantry plate connects to the x-axis beam above it with linear wheels and it connects to the y-axis beam below it with linear wheels. 2 extra wheels (bearings only) will engage with a nobby on each carriage.

RGB LED Strip across the underside of the y-axis gantry. Umbilical cord from the top center down to center of the y-axis gantry.


## Cover
[Twin wall polycarbonate roofing](https://www.bunnings.co.nz/twinwall-8-x-2400-x-610mm-clear-polycarbonate-roofing_p0124718?store=9474&gclid=Cj0KCQjwteOaBhDuARIsADBqRehCLp3DZUIPm4RK3flJGLu8eTeC2iw4wb14_lYqLewhmDrlqb3sHxsaAi3mEALw_wcB&gclsrc=aw.ds)

Walls that are not long enough can be joined with the a [joiner](https://www.bunnings.co.nz/twinwall-2400-x-8mm-clear-h-jointer_p0124720).


## Bed
Bed needs to be changable. Bed Types:
- Heated Glass for 3D Printing
- MDF board for cnc, vinyl cutter and pottery
- Honeycomb bed for laser cutting

The 3D Printing bed is heated by a 220V silicone heating mat.
It will use HE0 (PA2) on the BTT Octopus pro to control the SSR
https://docs.vorondesign.com/build/electrical/v2_octopus_wiring.html#ssr-wiring


The bed moves up and down (Z direction) starting at the top and moving down for 3D printing toolheads.
Quad gantry leveling is used to align the bed.
All 4 vertical actuators provide the vertical frame supports for the machine.


## Tools
List of tools:
- PLA Filament tool colour 1
- PLA Filament tool colour 2
- PETG Filament tool
- PVA Filament tool
- ABS Filament tool
- TPU Filament tool
- Probe tool
- Camera tool
- 3D Scanner tool
- Vinyl Cutter tool
- Paintbrush tool
- Laser cutter toolh
- Cake Icing tool
- CNC tool (with vacuum brush head)
  - Connects to x and z gantries to provide extra stability.
  - Attaches to gantries from the corner
- Laser Cutter tool
- Inkjet tool
- Clay printer tool
- Pick and Place Tool (Electrical Component placement)
- Robotic arm tool
- Electrical wire printer tool
- Electrical Soldering tool

Umbilical cords carry electrical wires, filament, air pipes and whatever else is needed from the center of the machine overhead to each tool. PTFE pipes will be used for the umbilical cords.

### Each Tool
Tools will be built on CANBUS boards
https://biqu.equipment/products/bigtreetech-ebb-36-42-can-bus-for-connecting-klipper-expansion-device?variant=39760665182306
https://github.com/bigtreetech/EBB
This allows for many tools to be connected to a single CANBUS through BTT Octopus pro canbus bridge.
Tool changer does not need to change electronic connections.
BTT EBB36/42

add filament motion sensor
https://www.printables.com/model/137999-diy-filament-motion-sensor


CanBus terminal resistors
Octopus pro must have 120ohm resistor
Add 120ohm resistors to the end of the twisted pair.
https://e2e.ti.com/support/interface-group/interface/f/interface-forum/850222/sn65hvd251-can-bus-termination


GCode for adjusting steppers indipendantly so that multiple steppers on a shared axis can be calibrated.
https://www.klipper3d.org/G-Codes.html#force_move_1


### Tool Docks and Berth
There are 2 docks. One along the front and another along the back.
Each tool will park in its own tool berth along one of the docks.
The tool docks are mounted to the top of the front and back x-axis 


### Filament tools
- https://www.bondtech.se/product/lgx-ace-mosquito-printhead/
- BTT H2 V2S Revo Extruder

Large diameter PTFE tube for filament. Allow hot air to flow out through PTFE tube to preheat filament.

https://www.aliexpress.com/item/32730855848.html?_randl_currency=NZD&_randl_shipto=NZ&src=google&memo1=freelisting&src=google&albch=shopping&acnt=494-037-6276&slnk=&plac=&mtctp=&albbt=Google_7_shopping&albagn=888888&isSmbAutoCall=false&needSmbHouyi=false&albcp=9444695485&albag=99457316601&trgt=1459734606882&crea=en32730855848&netw=u&device=c&albpg=1459734606882&albpd=en32730855848&gclid=Cj0KCQjwhsmaBhCvARIsAIbEbH4zDrgT9jA4TWF1_hX97Ajxq-JhdDpC8_BkMOKl3fPxQT5BdpYAEKAaApLEEALw_wcB&gclsrc=aw.ds&aff_fcid=d15cdb6bbaff43378d590866d32d7114-1666416491270-01265-UneMJZVf&aff_fsk=UneMJZVf&aff_platform=aaf&sk=UneMJZVf&aff_trace_key=d15cdb6bbaff43378d590866d32d7114-1666416491270-01265-UneMJZVf&terminal_id=55d5318285104dbd81f90e38987a2cba&afSmartRedirect=y

Large diameter silicon tube to push

Filament tool cabling summary
- 18 agw, 2 core silicon
- 22 agw twisted pair
- 8mm PTFE Tube


### Vinyl Cutter Tool
Cricut cutter


### Paintbrush Tool
Extra 2 degrees of freedom to tilt angle of paint brush


## Sensors and attachments

### Smoke Detection Sensor
This provides feedback for possible fire so that the printer can be turned off and an alarm raised.

### Probe Tool
A contact sensor provides micron accuracy of tool height for all tools. This allows the bed level sensor to be calibrated with all other sensors using the highest accuracy contact sensor. This accuracy is independant of bed type because all sensing is done with contact sensors.

### Filament tool brush
Separate component to the side for cleaning tools

### Cameras
Record video, timelapse and photographs

### Chamber Heater
Heating element
Heating fan
Chamber temperature sensor

https://www.aliexpress.com/item/1005001737139798.html?spm=a2g0o.detail.0.0.69d51cacsq7ZMD&gps-id=pcDetailBottomMoreThisSeller&scm=1007.13339.291025.0&scm_id=1007.13339.291025.0&scm-url=1007.13339.291025.0&pvid=f5336a29-bdae-4944-9390-a1a41320cee5&_t=gps-id:pcDetailBottomMoreThisSeller,scm-url:1007.13339.291025.0,pvid:f5336a29-bdae-4944-9390-a1a41320cee5,tpp_buckets:668%232846%238113%231998&pdp_ext_f=%7B%22sku_id%22%3A%2212000017392285956%22%2C%22sceneId%22%3A%223339%22%7D&pdp_npi=2%40dis%21NZD%2130.98%2130.98%21%21%21%21%21%402103239b16664227929741405ea123%2112000017392285956%21rec

Suck cold air out the chamber from the bottom.
Blow hot air in the chamber near the top.
Chamber temperature sensor under the bed
Chamber temperature sensor near the top
Chamber temperature sensor near the bottom


## Electronics box

### Cover
Polycarbonate sheeting for cover

### Motherboard
BigTreeTech Octopus Pro

pin names
https://teamgloomy.github.io/btt_octopus_pro_1.0_f429_pins.html

Pin config
- Remove usb C power selection jumper on MB
- Set SPI mode for drivers on MB
- Set en, step, dir pin names on printer cfg
- Set Motor voltage pins on MB


Use btt pi gpio pins for carriage sensors.
Each carriage has a switch that serves a sensor that determines that the carriage is loaded.

Use PB7 for touch probe



### Power Supply


#### 24 Volt Power Supply
Mean Well LRS-350-24
Mac 350 Watts
https://www.aliexpress.com/item/4000356081734.html

Power requirements
Drives the z steppers because they are slow 
Motors:  4 x 1.2 amps = 4.8 Amps
Motherboard = 1 amp
Other = 2 Amps
Filament Dryer Heater = 4 Amps


Sub Total = 11.8 amps
Safety Factor 10%
Total = 13 amps
13A x 24V = 312 Watts
350 W - 312 W = 38 Watts remaining

#### 48 Volt Power Supply
SE-600-48 Mean Well 600W/12.5A/48V DC Single Output Power Supply
https://www.aliexpress.com/item/4000390635110.html


Power requirement
Drives the x & y steppers because they require higher speed
HV Motors: 4 x 2 amps = 8 amps

Sub Total = 8 amps
Safety Factor 10%
Total = 10 amps

10A x 48V = 480 Watts
480 Watts


#### AC Power Supply
240 Watts - Mean Well LRS-350-24
480 Watts - Mean Well SE-600-48

Sub Total 720 Watts
240 Volts 
3 Amps


### Shutdown Module
BIGTREETECH Relay V1.2 Automatic Shutdown Module
https://www.youtube.com/watch?v=5wJff-hY90s

https://github.com/bigtreetech/BIGTREETECH-Relay-V1.2/issues/1

Normally open push button

### UPS Module
BTT UPS 24V V1.0 Resume Printing While Power Off Module

### Filament Dryer


## Wiring

Wall Socket -> Shutdown Module : Power supply cable

Shutdown Module -> 24V Power supply : 16 agw, 2 core
Shutdown Module | PSU on pins -> BTT Octopus Pro PSU On pins : Thin cable
Shutdown Module | 5v rst pins -> Normally open push button
Wall Socket -> 48V Power supply : Power supply cable
24V Power supply -> BTT Octopus Pro Power: 16 agw, 2 core
BTT Octopus Pro UPS Pin -> UPS Module : Provided Cable
48V Power supply -> BTT Octopus Pro : 16 agw, 2 core
BTT Octopus Pro -> EBB toolhead : power 18 agw, 2 core silicon, canh/l 24 agw
BTT Octopus Pro -> Nema23 motors : 22 agw silicon wires shielded 8 core (extra 2 for limit switch and 2 for cooling fan)
BTT Octopus Pro -> Chamber Heater : 240V
BTT Octopus Pro -> Chamber temperature Sensor : 24 agw
BTT Octopus Pro -> Filament Dryer Temperature Sensor : 24 agw
BTT Octopus Pro -> Filament Dryer fan : 24 agw


https://www.aliexpress.com/item/1005001732356744.html?spm=a2g0o.productlist.0.0.2a9668eehXHEF0&algo_pvid=c2463b0e-fe50-4855-8b70-8a39056fa019&algo_exp_id=c2463b0e-fe50-4855-8b70-8a39056fa019-3&pdp_ext_f=%7B%22sku_id%22%3A%2212000029019902332%22%7D&pdp_npi=2%40dis%21NZD%215.93%215.04%21%21%211.22%21%21%40210318cf16664135231422745e70c9%2112000029019902332%21sea&curPageLogUid=twhreFYSkeQF


Wire Gauge
16 agw -> 22 Amps
18 agw -> 16 Amps
22 agw -> 7 Amps
24 agw -> 3.5 Amps

## Homing
Override homing
Home X Axis first
Move along X to avoid probe carriage
Home Y Axis
Dock Probe carriage
Home Z


Probe Diameter

455.170156275233, 37.00000000051885, 8.999999999978172
437.4185937713502, 37.00000000051885, 8.999999999978172

327.41796874894015, 37.00000000051885, -0.9771875000218826
327.41796874894015, 37.00000000051885, 10.958046875125703


10.958046875125703 + 0.9771875000218826 = 11.935234375147583
455.170156275233 - 437.4185937713502 = 17.7515625038828

17.7515625038828 - 11.935234375147583 = 5.81632812873522



46.68656250197806, 68.00000000074303, 5.999999999958164
40.53781250177989, 68.00000000074303, 5.999999999958164

46.68656250197806 - 40.53781250177989 = 6.14875000019817
6.14875000019817 - 5.81632812873522 = 0.33242187146295
# 3D Printer Design

The purpose of this document is to provide details for design decision sand references

## General Design

Crossed Gantry

## Chamber
Fully enclosed and insulated chamber.
Possible clear to provide visibility of operation to increase ability to fix. Visible feedback.
Vacume holes at the base of chamber to suck of cnc debris.
Suck air in the bottom of the chamber and introduce hot air near the top.
The temperature of 3D printed polymers needs to be kept just below the Glass transition temprature to increase the bonding.
https://3dsolved.com/3d-filament-glass-transition-temperatures/


## Frame
2 motors for each horizontal axis increases force applied to each axis.
Nema 23 motors for higher forces
BTT Octopus pro with TMC5160 Pro so that Voltage can be increased to 48V for higher speeds and higher amps.

The actuators that drive the gantry beams are also the frame for the machine.
The gantry only moves in the x and y directions, while the bed moves in the z direction.

4 x z-axis linear actuators to move the bed vertically.
Vertical linear actuators also form the vertical frame.
Vertical linear actuators are C-Beam extrusions with stepper motors mounted at the bottom.
Stepper motors at the bottom are also the feet for the printer. Placing steppers at the top will get in the way and will be inside the heated chamber. Placing vertical steppers at the bottom will be outsode the heated chamber an therefore cooler.


## Gantry
Crossed Gantry
Each toolhead has its own roller. Only 1 degree of movement requires engaging.



## Cover
Twin wall polycarbonate roofing
https://www.bunnings.co.nz/twinwall-8-x-2400-x-610mm-clear-polycarbonate-roofing_p0124718?store=9474&gclid=Cj0KCQjwteOaBhDuARIsADBqRehCLp3DZUIPm4RK3flJGLu8eTeC2iw4wb14_lYqLewhmDrlqb3sHxsaAi3mEALw_wcB&gclsrc=aw.ds

join
https://www.bunnings.co.nz/twinwall-2400-x-8mm-clear-h-jointer_p0124720

## Bed
Bed is heated indirectly by air heater at the top of the printer. This has the affect of heating the entire insulated chamber.
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
- Paintbrush toolhead
- CNC toolhead (with vacuum brush head)
  - Connects to x and z gantries to provide extra stability.
  - Attaches to gantries from the corner
- Laser Cutter toolhead
- Inkjet toolhead
- Clay printer toolhead
- Pick and Place Toolhead (Electrical Component placement)
- Robotic arm toolhead
- Electrical wire printer toolhead
- Electrical Soldering toolhead

Place toolheads with an umbilical cable near the corners, so that the umbilical cables are pulled out of the way when the tool head is docked.

### Each Toolhead
Toolheads will be built on CANBUS boards
https://biqu.equipment/products/bigtreetech-ebb-36-42-can-bus-for-connecting-klipper-expansion-device?variant=39760665182306
This allows for many toolheads to be connected to a single CANBUS through BTT Octopus pro canbus bridge.
toolhead changer does not need to change electronic connections.
BTT EBB36/42

CanBus terminal resistors
Only the 2 end toolheads will have 120ohm resistors
octopus pro and end of the twisted pair.
https://e2e.ti.com/support/interface-group/interface/f/interface-forum/850222/sn65hvd251-can-bus-termination



### Filament toolheads
- https://www.bondtech.se/product/lgx-ace-mosquito-printhead/

Large diameter PTFE tube for filament. Allow hot air to flow out through PTFE tube to preheat filament.

https://www.aliexpress.com/item/32730855848.html?_randl_currency=NZD&_randl_shipto=NZ&src=google&memo1=freelisting&src=google&albch=shopping&acnt=494-037-6276&slnk=&plac=&mtctp=&albbt=Google_7_shopping&albagn=888888&isSmbAutoCall=false&needSmbHouyi=false&albcp=9444695485&albag=99457316601&trgt=1459734606882&crea=en32730855848&netw=u&device=c&albpg=1459734606882&albpd=en32730855848&gclid=Cj0KCQjwhsmaBhCvARIsAIbEbH4zDrgT9jA4TWF1_hX97Ajxq-JhdDpC8_BkMOKl3fPxQT5BdpYAEKAaApLEEALw_wcB&gclsrc=aw.ds&aff_fcid=d15cdb6bbaff43378d590866d32d7114-1666416491270-01265-UneMJZVf&aff_fsk=UneMJZVf&aff_platform=aaf&sk=UneMJZVf&aff_trace_key=d15cdb6bbaff43378d590866d32d7114-1666416491270-01265-UneMJZVf&terminal_id=55d5318285104dbd81f90e38987a2cba&afSmartRedirect=y

Large diameter silicon tube to push

Filament toolhead cabling summary
- 18 agw, 2 core silicon
- 22 agw twisted pair
- 8mm PTFE Tube


### Vinyl Cutter Toolhead



### Paintbrush Toolhead
Extra 2 degrees of freedom to tilt angle of paint brush


## Sensors and attachments

### Smoke Detection Sensor
This provides feedback for possible fire so that the printer can be turned off and an alarm raised.

### Toolhead level sensor
A contact sensor provides micron accuracy of toolhead height for all toolheads. This allows the bed level sensor to be calibrated with all other sensors using the highest accuracy contact sensor. This accuracy is independant of bed type because all sensing is done with contact sensors.

### Filament toolhead cleaner
Separate component to the side for cleaning toolheads

### Cameras
Take video and photographs

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
BigTreeTech Ocotopius Pro


### Power Supply

#### 24 Volt Power Supply
Mean Well LRS-350-24
https://www.aliexpress.com/item/4000356081734.html

Power requirements
Motors:  4 x 2.8 amps = 11.2 amps
Motherboard = 1 amp
Other = 2 Amp

Sub Total = 11 amps
Safety Factor 20%
Total = 13.2 amps
13.2A x 24V = 316 Watts

#### 48 Volt Power Supply
SE-600-48 Mean Well 600W/12.5A/48V DC Single Output Power Supply
https://www.aliexpress.com/item/4000390635110.html


Power requirements
HV Motors: 4 x 2.8 amps = 11.2 amps

Sub Total = 11.2 amps
Safety Factor 20%
Total = 13.5 amps

13.5A x 48V = 648 Watts
645 Watts

Safety Factor 10%
Total = 12.5 amps
600Watts


### Shutdown Module
BIGTREETECH Relay V1.2 Automatic Shutdown Module
https://www.youtube.com/watch?v=5wJff-hY90s

Normally open push button


### UPS Module
BTT UPS 24V V1.0 Resume Printing While Power Off Module





## Wiring

Wall Socket -> Shutdown Module : Power supply cable

Shutdown Module -> 24V Power supply : 16 agw, 2 core
Shutdown Module | PSU on pins -> BTT Octopus Pro PSU On pins : Thin cable
Shutdown Module | 5v rst pins -> Normally open push button
Wall Socket -> 48V Power supply : Power supply cable
24V Power supply -> BTT Octopus Pro Power: 16 agw, 2 core
BTT Octopus Pro UPS Pin -> UPS Module : Provided Cable
48V Power supply -> BTT Octopus Pro : 16 agw, 2 core
BTT Octopus Pro -> EBB toolhead : power 18 agw, 2 core silicon, canh/l 22 agw
BTT Octopus Pro -> Nema23 motors : 22 agw silicon wires shielded 4 core
BTT Octopus Pro -> Chamber Heater : 
BTT Octopus Pro -> Chamber temperature Sensor : Cat5e


https://www.aliexpress.com/item/1005001732356744.html?spm=a2g0o.productlist.0.0.2a9668eehXHEF0&algo_pvid=c2463b0e-fe50-4855-8b70-8a39056fa019&algo_exp_id=c2463b0e-fe50-4855-8b70-8a39056fa019-3&pdp_ext_f=%7B%22sku_id%22%3A%2212000029019902332%22%7D&pdp_npi=2%40dis%21NZD%215.93%215.04%21%21%211.22%21%21%40210318cf16664135231422745e70c9%2112000029019902332%21sea&curPageLogUid=twhreFYSkeQF



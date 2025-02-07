class MultiHeatBed:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.heater_areas = float(config.get('hot_zone_retract_length') or 20)
        self.hot_zone_retract_speed = float(config.get('hot_zone_retract_speed') or 80)
        self.retract_xy_wiggle = float(config.get('retract_xy_wiggle') or 2)
        self.retract_z = float(config.get('retract_z') or 0.1)
        self.printer.add_object('retraction', self)


def load_config(config):
    return MultiHeatBed(config)







[gcode_macro HEATBED_AUTO]
variable_parameter_AREA_START : 0,0
variable_parameter_AREA_END : 0,0
gcode:

#Set the coordinates of the heatbed sections
    {% set x0 = 0 %}
    {% set x1 = 100 %}
    {% set x2 = 200 %}
    {% set x3 = 300 %}
    {% set x4 = 400 %}

    {% set y0 = 0 %}
    {% set y1 = 105 %}
    {% set y2 = 210 %}
#Get parameters from Slicer
    {% set BED_TEMP = params.BED_TEMP|default(50)|float %}
    {% if params.AREA_START and params.AREA_END %}
        {% set A = params.AREA_START.split(",")[0]|float %}
    	{% set B = params.AREA_START.split(",")[1]|float %}
    	{% set C = params.AREA_END.split(",")[0]|float %}
    	{% set D = params.AREA_END.split(",")[1]|float %}

#Check and enable the required heatbeds
    #Heatbed 1  x1,y0  x2,y1
        {% if ((C > x1) and (D > y0) and (A < x2) and (B < y1)) %}
            SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET={BED_TEMP}        
        {% endif %}
    #Heatbed 2  x0,y0  x1,y1
        {% if ((C > x0) and (D > y0) and (A < x1) and (B < y1)) %}
            SET_HEATER_TEMPERATURE HEATER=heater_bed2 TARGET={BED_TEMP}         
        {% endif %}
    #Heatbed 3  x0,y1  x1,y2
        {% if ((C > x0) and (D > y1) and (A < x1) and (B < y2)) %}
            SET_HEATER_TEMPERATURE HEATER=heater_bed3 TARGET={BED_TEMP}         
        {% endif %}
    #Heatbed 4  x1,y1  x2,y2
        {% if ((C > x1) and (D > y1) and (A < x2) and (B < y2)) %}
            SET_HEATER_TEMPERATURE HEATER=heater_bed4 TARGET={BED_TEMP}        
        {% endif %}
    #Heatbed 5  x2,y1  x3,y2
        {% if ((C > x2) and (D > y1) and (A < x3) and (B < y2)) %}
            SET_HEATER_TEMPERATURE HEATER=heater_bed5 TARGET={BED_TEMP}         
        {% endif %}
    #Heatbed 6  x3,y1  x4,y2
        {% if ((C > x3) and (D > y1) and (A < x4) and (B < y2)) %}
            SET_HEATER_TEMPERATURE HEATER=heater_bed6 TARGET={BED_TEMP}         
        {% endif %}
    #Heatbed 7  x3,y0  x4,y1
        {% if ((C > x3) and (D > y0) and (A < x4) and (B < y1)) %}
            SET_HEATER_TEMPERATURE HEATER=heater_bed7 TARGET={BED_TEMP}        
        {% endif %}
    #Heatbed 8  x2,y0  x3,y1
        {% if ((C > x2) and (D > y0) and (A < x3) and (B < y1)) %}
            SET_HEATER_TEMPERATURE HEATER=heater_bed8 TARGET={BED_TEMP}         
        {% endif %}
    {% endif %}
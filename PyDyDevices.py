            
#          #cmd   # name                  #length of value
dictAXCmd = { 0  : ["MODEL_NUMBER_L        ",2],
            1  : ["MODEL_NUMBER_H        ",1],
            2  : ["VERSION               ",1],
            3  : ["SERVO_ID              ",1],
            4  : ["BAUD_RATE             ",1],
            5  : ["RETURN_DELAY_TIME     ",1],
            6  : ["CW_ANGLE_LIMIT_L      ",2],
            7  : ["CW_ANGLE_LIMIT_H      ",1],
            8  : ["CCW_ANGLE_LIMIT_L     ",2],
            9  : ["CCW_ANGLE_LIMIT_H     ",1],
            10 : ["BAD(10)               ",1], #10 (Reserved) # See pg 12/18 of manual
            11 : ["LIMIT_TEMPERATURE     ",1],
            12 : ["LOW_LIMIT_VOLTAGE     ",1],
            13 : ["HIGH_LIMIT_VOLTAGE    ",1],
            14 : ["MAX_TORQUE_L          ",2],
            15 : ["MAX_TORQUE_H          ",1],
            16 : ["STATUS_RETURN_LEVEL   ",1],
            17 : ["ALARM_LED             ",1],
            18 : ["ALARM_SHUTDOWN        ",1],
            19 : ["BAD(19)               ",1], #19 (Reserved) # See pg 12/18 of manual
            20 : ["DOWN_CALIBRATION_L    ",2], # Read-only/not used
            21 : ["DOWN_CALIBRATION_H    ",1], # Read-only/not used
            22 : ["UP_CALIBRATION_L      ",2], # Read-only/not used
            23 : ["UP_CALIBRATION_H      ",1], # Read-only/not used
            24 : ["TORQUE_ENABLE         ",1],
            25 : ["LED                   ",1],
            26 : ["CW_COMPLIANCE_MARGIN  ",1],
            27 : ["CCW_COMPLIANCE_MARGIN ",1],
            28 : ["CW_COMPLIANCE_SLOPE   ",1],
            29 : ["CCW_COMPLIANCE_SLOPE  ",1],
            30 : ["GOAL_POSITION_L       ",2],
            31 : ["GOAL_POSITION_H       ",1],
            32 : ["GOAL_SPEED_L          ",2],
            33 : ["GOAL_SPEED_H          ",1],
            34 : ["TORQUE_LIMIT_L        ",2],
            35 : ["TORQUE_LIMIT_H        ",1],
            36 : ["PRESENT_POSITION_L    ",2],
            37 : ["PRESENT_POSITION_H    ",1],
            38 : ["PRESENT_SPEED_L       ",2],
            39 : ["PRESENT_SPEED_H       ",1],
            40 : ["PRESENT_LOAD_L        ",2],
            41 : ["PRESENT_LOAD_H        ",1],
            42 : ["PRESENT_VOLTAGE       ",1],
            43 : ["PRESENT_TEMPERATURE   ",1],
            44 : ["REGISTERED_INSTRUCTION",1],
            46 : ["MOVING                ",1],
            47 : ["LOCK                  ",1],
            48 : ["PUNCH_L               ",2],
            49 : ["PUNCH_H               ",1],
            56 : ["BAD(56)               ",0], # EX-106+ only
            57 : ["BAD(57)               ",0], # EX-106+ only
            70 : ["BAD(70)               ",0], # MX-64/106 only
            71 : ["BAD(71)               ",0], # MX-64/106 only
            72 : ["BAD(72)               ",0], # MX-64/106 only
            73 : ["BAD(73)               ",0]  # MX only
            }

dictAX12WCmd = dictAXCmd.copy()
dictAX18Cmd = dictAXCmd.copy()

dictRX24Cmd = dictAXCmd.copy()
dictRX28Cmd = dictAXCmd.copy()
dictRX64Cmd = dictAXCmd.copy()

dictMX28Cmd = dictAXCmd.copy()
dictMX28Cmd[26] = ["D_GAIN                ",1],
dictMX28Cmd[27] = ["I_GAIN                ",1],
dictMX28Cmd[28] = ["P_GAIN                ",1],
dictMX28Cmd[29] = ["BAD(29)               ",1],
dictMX28Cmd[73] = ["GOAL_ACCELERATION     ",0]
  
dictMX64Cmd = dictMX28Cmd.copy()
dictMX64Cmd[70] = ["TORQUE_CONTROL_ENABLE ",1]
dictMX64Cmd[71] = ["GOAL_TORQUE_L         ",2]
dictMX64Cmd[72] = ["GOAL_TORQUE_H         ",1]

dictMX106Cmd = dictMX64Cmd.copy()         

dictEX106Cmd = dictAXCmd.copy()    
dictEX106Cmd[56] = ["SENSED_CURRENT_L      ",2]
dictEX106Cmd[57] = ["SENSED_CURRENT_H      ",1]
            
#          #cmd   # name                  #length of value 
dictAXS1Cmd = { 0  : ["MODEL_NUMBER_L        ",2],
            1  : ["MODEL_NUMBER_H        ",1],
            2  : ["VERSION               ",1],
            3  : ["SERVO_ID              ",1],
            4  : ["BAUD_RATE             ",1],
            5  : ["RETURN_DELAY_TIME     ",1],
            6  : ["BAD(6)                ",0], # (Reserved) # See pg 13 of manual
            7  : ["BAD(7)                ",0], # (Reserved) # See pg 13 of manual
            8  : ["BAD(8)                ",0], # (Reserved) # See pg 13 of manual
            9  : ["BAD(9)                ",0], # (Reserved) # See pg 13 of manual
            10 : ["BAD(10)               ",0], # (Reserved) # See pg 13 of manual
            11 : ["LIMIT_TEMPERATURE     ",1],
            12 : ["LOW_LIMIT_VOLTAGE     ",1],
            13 : ["HIGH_LIMIT_VOLTAGE    ",1],
            14 : ["BAD(14)               ",0], # (Reserved) # See pg 13 of manual
            15 : ["BAD(15)               ",0], # (Reserved) # See pg 13 of manual
            16 : ["STATUS_RETURN_LEVEL   ",1],
            17 : ["BAD(17)               ",0], # (Reserved) # See pg 13 of manual
            18 : ["BAD(18)               ",0], # (Reserved) # See pg 13 of manual
            19 : ["BAD(19)               ",0], # (Reserved) # See pg 13 of manual
            20 : ["OBST_DETECTD_COMP_VAL ",1],
            21 : ["LIGHT_DETECTD_COMP_VAL",1],
            22 : ["BAD(22)               ",0], # (Reserved) # See pg 13 of manual
            23 : ["BAD(23)               ",0], # (Reserved) # See pg 13 of manual
            24 : ["BAD(24)               ",0], # (Reserved) # See pg 13 of manual
            25 : ["BAD(25)               ",0], # (Reserved) # See pg 13 of manual
            26 : ["LEFT_IR_SENSOR_DATA   ",1],
            27 : ["CENTER_IR_SENSOR_DATA ",1],
            28 : ["RIGHT_IR_SENSOR_DATA  ",1],
            29 : ["LEFT_LUMINOSITY       ",1],
            30 : ["CENTER_LUMINOSITY     ",2],
            31 : ["RIGHT_LUMINOSITY      ",1],
            32 : ["OBSTACLE_DETECT_FLAG  ",2],
            33 : ["LUMINOSITY_DETECT_FLAG",1],
            34 : ["BAD(34)               ",0], # (Reserved) # See pg 13 of manual
            35 : ["SOUND_DATA            ",1],
            36 : ["SOUND_DATA_MAX_HOLD   ",1],
            37 : ["SOUND_DETECTED_COUNT  ",1],
            38 : ["SOUND_DETECTED_TIME_L ",2],
            39 : ["SOUND_DETECTED_TIME_H ",1],
            40 : ["BUZZER_INDEX          ",1],
            41 : ["BUZZER_TIME           ",1],
            42 : ["PRESENT_VOLTAGE       ",1],
            43 : ["PRESENT_TEMPERATURE   ",1],
            44 : ["REGISTERED_INSTRUCTION",1],
            45 : ["BAD(45)               ",0], # (Reserved) # See pg 13 of manual
            46 : ["IR_REMOCON_ARRIVED    ",1],
            47 : ["LOCK                  ",1],
            48 : ["IR_REMOCON_RX_DATA_0  ",1],
            49 : ["IR_REMOCON_RX_DATA_1  ",1],
            50 : ["IR_REMOCON_TX_DATA_0  ",1],
            51 : ["IR_REMOCON_TX_DATA_1  ",1],
            52 : ["OBSTACLE_DETECTED_COMP",1],
            53 : ["LIGHT_DETECTED_COMPARE",1]
            }
    
        
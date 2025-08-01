# Climbing Robot Control System

A Raspberry Pi-based climbing robot capable of autonomously climbing vertical poles of different diameters using pneumatic actuators, servos, and ultrasonic sensing.

## 🤖 Overview

This climbing robot uses a sophisticated control system with:
- **Radial actuators** for gripping poles
- **Horizontal actuators** for positioning
- **Vertical actuator** for climbing motion
- **Servo motors** for directional control
- **Ultrasonic sensor** for height measurement
- **PID control** for precise movement

## 📋 Hardware Requirements

### Electronics
- Raspberry Pi (with GPIO access)
- HC-SR04 Ultrasonic Distance Sensor
- 2x Servo Motors (connected to GPIO 12 and 13)
- Multiple relay modules for actuator control
- Power supply for actuators

### Mechanical Components
- Upper and lower radial pneumatic actuators
- Upper and lower horizontal pneumatic actuators  
- Vertical pneumatic actuator
- Mechanical gripping mechanism

## 🔌 Pin Configuration

| Component | GPIO Pin | Function |
|-----------|----------|----------|
| Upper Radial Extend | 18 | Control upper radial actuator extension |
| Upper Radial Retract | 19 | Control upper radial actuator retraction |
| Lower Radial Extend | 20 | Control lower radial actuator extension |
| Lower Radial Retract | 21 | Control lower radial actuator retraction |
| Upper Horizontal Extend | 22 | Control upper horizontal actuator extension |
| Upper Horizontal Retract | 23 | Control upper horizontal actuator retraction |
| Lower Horizontal Extend | 24 | Control lower horizontal actuator extension |
| Lower Horizontal Retract | 25 | Control lower horizontal actuator retraction |
| Upper Servo | 12 | Upper servo motor control |
| Lower Servo | 13 | Lower servo motor control |
| Vertical Extend | 26 | Vertical actuator extension |
| Vertical Retract | 16 | Vertical actuator retraction |
| Ultrasonic Trigger | 27 | Distance sensor trigger |
| Ultrasonic Echo | 17 | Distance sensor echo |

## 📦 Installation

### Dependencies
```bash
# Install required Python packages
pip install RPi.GPIO simple-pid
```

### File Structure
```
climbing-robot/
├── robot.py              # Main robot control class
├── up.py                 # Upward climbing control
├── down.py               # Downward climbing control
├── adjust_servo.py       # Servo position adjustment
├── retract_test.py       # Initial retraction testing
├── extend_test.py        # Final extension testing
├── ultrasonic_test.py    # Distance sensor testing
├── vertical_test.py      # Vertical actuator testing
├── *_test.py             # Individual component tests
└── README.md
```

## 🚀 Usage

### Basic Climbing Operations

#### Upward Climbing
```bash
# Climb to 120cm height
python3 up.py

# Initialize for 30cm diameter pole and climb
python3 up.py -r 30

# Initialize for 60cm diameter pole and climb
python3 up.py -r 60
```

#### Downward Climbing
```bash
# Descend to ground level
python3 down.py
```

### Initial Setup for Different Pole Diameters

#### 30cm Diameter Pole
```bash
python3 retract_test.py -r 30
```

#### 60cm Diameter Pole
```bash
python3 retract_test.py -r 60
```

### Component Testing

Test individual components before full operation:

```bash
# Test ultrasonic distance sensor
python3 ultrasonic_test.py

# Test vertical actuator
python3 vertical_test.py

# Test servo motors
python3 lower_servo_test.py
python3 upper_servo_test.py

# Test radial actuators
python3 lower_radius_test.py
python3 upper_radius_test.py

# Test horizontal actuators
python3 lower_horizontal_test.py
python3 upper_horizontal_test.py
```

### Final Operations

```bash
# Release from pole and retract all actuators
python3 extend_test.py

# Adjust servo to 90-degree position
python3 adjust_servo.py
```

## 🎛️ Control Parameters

### PID Control Settings
- **Kp**: 0.02 (Proportional gain)
- **Ki**: 0.001 (Integral gain)  
- **Kd**: 0.01 (Derivative gain)
- **Output Limits**: 0.5-3.0 seconds

### Timing Parameters
- **30cm Pole Retraction**: 3.0s (radial), 1.5s (horizontal)
- **60cm Pole Retraction**: 10.0s (radial), 1.0s (horizontal)
- **Climbing Extension**: 3.0s
- **Servo Rotation**: 0.5s
- **Final Release**: 20.0s (radial), 6.0s (horizontal)

## 🔄 Climbing Algorithm

### Upward Climbing Sequence
1. **Even steps** (Upper actuator):
   - Extend upper radial actuator
   - Rotate upper servo counterclockwise
   - Extend vertical actuator
   - Rotate upper servo clockwise
   - Retract upper radial actuator

2. **Odd steps** (Lower actuator):
   - Extend lower radial actuator
   - Rotate lower servo counterclockwise
   - Extend vertical actuator
   - Rotate lower servo clockwise
   - Retract lower radial actuator

### Downward Climbing Sequence
Similar to upward but with reversed vertical movement (retraction instead of extension).

## 🛡️ Safety Features

- **Emergency Stop**: Immediately stops all actuators and resets servos
- **Height Monitoring**: Continuous ultrasonic distance measurement
- **Progress Verification**: Checks if robot is making climbing progress
- **GPIO Cleanup**: Proper resource cleanup on exit
- **Error Handling**: Comprehensive exception handling

## 🔧 Configuration

### Pole Diameter Settings
The robot supports two pole diameter configurations:

- **30cm poles**: Optimized retraction times and parameters
- **60cm poles**: Extended retraction times for larger diameter

### PID Tuning
Adjust PID parameters in the controller classes:
```python
self.height_pid = PID(Kp=0.02, Ki=0.001, Kd=0.01, setpoint=target_height)
```

## 📊 Monitoring and Logging

The system provides detailed logging including:
- Current height measurements
- PID control outputs
- Step-by-step climbing progress
- Error conditions and warnings
- Total climbing statistics

## 🐛 Troubleshooting

### Common Issues

1. **Servo not responding**
   - Check GPIO connections
   - Verify power supply
   - Run servo test scripts

2. **Ultrasonic sensor errors**
   - Check wiring to GPIO 27 (trigger) and 17 (echo)
   - Ensure clear line of sight
   - Run ultrasonic test

3. **Actuators not moving**
   - Verify relay connections
   - Check power supply to pneumatic system
   - Test individual actuators

4. **Robot not climbing**
   - Check initial pole grip with retraction test
   - Verify all actuators are functional
   - Ensure proper PID tuning

### Debug Mode
Enable detailed logging by setting log level to DEBUG:
```python
logging.basicConfig(level=logging.DEBUG)
```

## ⚠️ Important Notes

- Always test individual components before full climbing operation
- Ensure proper power supply for all actuators
- Initialize robot with correct pole diameter setting
- Monitor climbing progress and be ready to emergency stop
- Perform final extension to safely release from pole

## 🤝 Contributing

When modifying the code:
1. Test individual components first
2. Update timing parameters as needed for your hardware
3. Maintain logging for debugging
4. Follow the established error handling patterns

## 📄 License

This project is open source. Please ensure safe operation and proper testing before use.
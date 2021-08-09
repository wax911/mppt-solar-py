# Contents of Directory

## configuration.yaml

**File containing application configuration e.g.**
```yaml
device:
  interface: '/dev/hidraw0'
  baud_rate: 2400
  is_serial: false
mqtt:
  topic: 'voltronic/axpert_king'
  host: 'localhost'
  port: 1833
  username: 'USER_NAME'
  password: 'PASSWORD'
# One of the following: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
verbosity: 'DEBUG'
plugin: 'generic-inverter'
```
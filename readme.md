# File switcher

Switch file content based on pin state

## Pinout configuration

Open __switcher.py__ file and set variable __pin_to_filename_mapping__
to correct values. Keys of the dictionary are pin number of Raspberry Pi in BCM convention.
Check also if __boot_config_filename__ variable store filename of target configuration file.

## Service configuration

Open __switcher.service__ file and set the __ExecStart__ entry to
path to the __switcher.py__ file.

## Installation

1. Copy __switcher.service__ to /etc/systemd/system/  
    ```sudo cp switcher.service /etc/systemd/system/```

2. Change the owner of the service file to root user  
    ```sudo chown root:root /etc/systemd/system/switcher.service```

3. Grant rights to execute to the service file  
    ```sudo chmod 664 /etc/systemd/system/switcher.service```

4. Reload the service list  
    ```sudo systemctl daemon-reload```

5. Enable service  
    ```sudo systemctl enable switcher.service```

6. Start the service  
    ```sudo systemctl start irr.service```

## Electric circuit

```none
-----------
|         |
|         |--GND----O >----------+        ------------
|         |                      |        |          |
|         |--PIN-A--O >----+     +--< O---|   Two    |=========|
|   RPI   |                |              | Position |
|         |                +--------< O---|  Switch  |
|         |                               |          |
|         |--3.3V---O >----+--------< O---|          |
|         |                |              |          |
|         |                |              ------------
|         |                |
|         |                |
|         |                |              ------------
|         |                |              |          |
|         |                +--------< O---|   Two    |
|         |                               | Position |
|         |--PIN-B--O >-------------< O---|  Switch  |
|         |                               |          |=========|
|         |--GND----O > ------------< O---|          |
|         |                               |          |
-----------                               -----------
```
1. Open a terminal.

2. Update the package list by running the command:

    sudo apt update

3. Install the Mosquitto MQTT broker with the following command:

    sudo apt install mosquitto

4. Create and activate your virtual environment using this command:

    python3 -m venv .env
    source .env/bin/activate

5. Create a folder (I called mqtt) and 2 python files: mqtt_pub.py and mqtt_sub.py

    mkdir mqtt
    touch mqtt_pub.py
    touch mqtt_sub.py

6. Install Paho Client using the pip package manager:

    pip install paho-mqtt

7. And now we are ready for the code! 

8. mqtt_pub.py:

    nano mqtt_pub.py

9. mqtt_sub.py:

    nano mqtt_pub.py

10. În sfârșit executați în diferite terminale pentru a rula scripturile python
    
    python3 mqtt_sub.py
    python3 mqtt_pub.py
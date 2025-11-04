## Scripts Overview

**mux_tx_rx.py**  
- Provides a **SerialManager** class that handles sending and receiving data.  
- Can use real serial ports or simulate serial communication via files (`a_to_b.txt` and `b_to_a.txt`).  
- Supports assigning callback functions for received data.

**talker_mockup.py**  
- Demonstrates how `mux_tx_rx` works in **simulation mode**.  
- **Two instances** of the script should be run simultaneously to show how data are sent/received between two processes.

## How to Run

```
python talker_mockup.py -s -n <A|B>
```

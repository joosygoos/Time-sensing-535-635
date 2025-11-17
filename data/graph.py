import matplotlib.pyplot as plt
from datetime import datetime
import os

def generate_voltage_graph(filename="data.txt"):
    """
    Reads data in the format timestamp,voltage,timestamp,voltage,... from a file,
    parses it, and generates a time-series plot of voltage.
    """
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found. Please ensure the data file exists.")
        print("Tip: If you run this script in the same directory as the data.txt file, it should work.")
        return

    timestamps = []
    voltages = []
    
    # 1. Read and Parse the Data
    try:
        with open(filename, 'r') as f:
            # Read the entire content (which is a single long comma-separated string)
            content = f.read().strip()
            
        # Split the string by commas
        data_points = content.split(',')
        # About 7 minutes worth of samples
        samples = len(data_points) 
        data_points = data_points[10000:20000]
        # Iterate over the list in pairs: [timestamp, voltage, timestamp, voltage, ...]
        for i in range(0, len(data_points), 2):
            # The timestamp string is the element at index i
            ts_str = data_points[i].strip()
            # The voltage string is the element at index i+1
            v_str = data_points[i+1].strip()
            
            # --- UPDATED PARSING LOGIC ---
            # The timestamp is now a Unix epoch float (seconds since 1970).
            # Convert the string to a float first, then use fromtimestamp().
            time_obj = datetime.fromtimestamp(float(ts_str))
            
            # Convert voltage string to float
            voltage_val = float(v_str)
            
            timestamps.append(time_obj)
            voltages.append(voltage_val)

    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return
    except ValueError as e:
        # This will catch errors if the timestamp or voltage strings can't be converted to float
        # or if the timestamp is out of a valid range for datetime.
        print(f"Error parsing data. Check format or type conversion: {e}")
        return
    except IndexError:
        print("Error: Incomplete data pair found. Ensure all timestamps have a corresponding voltage.")
        return

    # 2. Plot the Data
    if not timestamps:
        print("No data was successfully parsed. Cannot generate graph.")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, voltages, marker='o', linestyle='-', color='teal')
    
    # Add labels and title
    plt.title("Voltage vs. Time Readout")
    plt.xlabel("Time (Timestamp)")
    plt.ylabel("Voltage (V)")
    plt.grid(True)
    plt.xticks(rotation=45, ha='right') # Rotate X-axis labels for readability
    plt.tight_layout() # Adjust layout to prevent labels from being cut off
    
    # Display the plot
    print(f"Successfully plotted {len(timestamps)} data points. Displaying graph...")
    plt.show()

if __name__ == "__main__":
    # Ensure you have matplotlib installed: pip install matplotlib
    generate_voltage_graph("audio/panashe_audio1.txt")



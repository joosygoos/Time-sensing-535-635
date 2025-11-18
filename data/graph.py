import matplotlib.pyplot as plt
from datetime import datetime
import os
import pandas as pd
import numpy as np

def calculate_rms(data_chunk: np.ndarray):
    """
    NOTE: EXPERIMENTAL, DONT KNOW IF WORKS, MY ATTEMPT AT CALCULATING DECIBELS

    Calculates the RMS value for a chunk of audio data.
    data_chunk should be a numpy array of voltage samples.
    """
    # First, center the signal if it has a DC offset (common with some sensors)
    # The baseline should be around 0.
    baseline = np.mean(data_chunk)
    centered_data = data_chunk - baseline

    # Calculate the RMS value
    rms = np.sqrt(np.mean(np.square(centered_data)))
    return rms

def rms_to_db(rms_value, reference_level):
    """
    NOTE: EXPERIMENTAL, DONT KNOW IF WORKS, MY ATTEMPT AT CALCULATING DECIBELS

    Converts an RMS value to a relative decibel (dB) level.
    """
    if rms_value == 0:
        return -np.inf # Avoid log(0) error
    # Use 20*log10 for amplitude/voltage
    db = -20.0 * np.log10(rms_value / reference_level)
    return db

def extract_decibels(window_data: np.ndarray):
    '''
    NOTE: EXPERIMENTAL, DONT KNOW IF WORKS, MY ATTEMPT AT CALCULATING DECIBELS
    '''
    rms = calculate_rms(window_data)
    db = rms_to_db(rms, 2.5)
    return db

def parse_file_to_dataframe(filename="data.txt"):
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
        ''' UNCOMMENT LINE BELOW TO USE ALL DATAPOINTS '''
        data_points = data_points[140000:220000]

        # Iterate over the list in pairs: [timestamp, voltage, timestamp, voltage, ...]
        for i in range(0, len(data_points), 2):
            # The timestamp string is the element at index i
            ts_str = data_points[i].strip()
            # The voltage string is the element at index i+1
            v_str = data_points[i+1].strip()
            
            # --- UPDATED PARSING LOGIC ---
            # The timestamp is now a Unix epoch float (seconds since 1970).
            # Convert the string to a float first, then use fromtimestamp().
            time_obj = (float(ts_str))
            
            # Convert voltage string to float
            voltage_val = float(v_str) * 0.75   # NOTE: I had calculation error in esp32 data collection, multiply by 0.75 to fix
            
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

    data_dict = {"Time": timestamps, "Voltage": voltages};
    df = pd.DataFrame(data_dict)
    df["Variation"] = df["Voltage"].rolling(window=500).var().rolling(window=1000).mean()
    df["Decibels"] = df["Voltage"].rolling(window=500).apply(extract_decibels, raw=True)

    df["Variation_Normalized"] = (df["Variation"] - df["Variation"].min()) / (df["Variation"].max() - df["Variation"].min())

    return df

if __name__ == "__main__":
    # Ensure you have matplotlib installed: pip install matplotlib, also do pip install pandas, pip install numpy

    '''
    UNCOMMENT LINES BELOW TO CHOOSE BETWEEN AUDIO AND PWM FILES
    NOTE: data_points = data_points[x:y] inside parse_file_to_dataframe DETERMINES RANGE OF POINTS TO GRAPH
    '''
    dataframe1 = parse_file_to_dataframe("audio/panashe_audio1.txt")
    dataframe2 = parse_file_to_dataframe("audio/joshua_audio1.txt")
    # dataframe1 = parse_file_to_dataframe("pwm/panashe_pwm1.txt")
    # dataframe2 = parse_file_to_dataframe("pwm/joshua_pwm1.txt")

    plt.figure(figsize=(10, 6))
    plt.plot(dataframe1["Time"].tolist(), dataframe1["Variation_Normalized"].tolist(), marker='o', linestyle='-', color='teal')
    plt.plot(dataframe2["Time"].tolist(), dataframe2["Variation_Normalized"].tolist(), marker='o', linestyle='-', color='red')
    
    # Add labels and title
    plt.title("Variation vs. Time Readout")
    plt.xlabel("Time (Seconds since Unix epoch)")
    plt.ylabel("Variation Normalized")
    plt.grid(True)
    plt.xticks(rotation=45, ha='right') # Rotate X-axis labels for readability
    plt.tight_layout() # Adjust layout to prevent labels from being cut off
    
    # Display the plot
    print(f"Successfully plotted {len(dataframe2["Time"].tolist())} data points. Displaying graph...")
    plt.show()

    '''
    SAVE DATAFRAMES
    UNCOMMENT TO CHOOSE BETWEEN PWM AND AUDIO FILES, BUT
    I RECOMMEND LEAVING THSE COMMENTED OUT TO NOT OVERRIDE OUR CSV FILES
    '''
    # dataframe1.to_csv("audio/panashe_audio1.csv", index=False) # index=False prevents saving the DataFrame index as a column
    # dataframe2.to_csv("audio/joshua_audio1.csv", index=False)
    # dataframe1.to_csv("pwm/panashe_pwm1.csv", index=False)
    # dataframe2.to_csv("pwm/joshua_pwm1.csv", index=False)


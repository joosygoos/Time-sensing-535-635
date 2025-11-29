import matplotlib.pyplot as plt
from datetime import datetime
import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

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

def match_peaks(peak_timestamps1, peak_values1, peak_timestamps2, peak_values2, max_offset):
    new_timestamps1 = []
    new_values1 = []
    new_timestamps2 = []
    new_values2 = []

    i = 0
    j = 0

    while(i < len(peak_timestamps1) and j < len(peak_timestamps2)):
        if abs(peak_timestamps1[i] - peak_timestamps2[j]) <= max_offset:
            new_timestamps1.append(peak_timestamps1[i])
            new_values1.append(peak_values1[i])
            new_timestamps2.append(peak_timestamps2[j])
            new_values2.append(peak_values2[j])
            i += 1
            j += 1

        elif peak_timestamps1[i] > peak_timestamps2[j]:
            j += 1
        else:
            i += 1

    assert(len(new_timestamps1) == len(new_values1))
    assert(len(new_values1) == len(new_timestamps2))
    assert(len(new_timestamps2) == len(new_values2))

    return new_timestamps1, new_values1, new_timestamps2, new_values2

def calculate_offset(peak_timestamps1, peak_values1, peak_timestamps2, peak_values2):
    """ Assumes the 4 list parameters are the same length, positive offset means second dataset has higher timestamps (ahead in time) """
    avg_offset = 0
    # avg_drift = 0

    for i in range(len(peak_timestamps1)):
        avg_offset += (peak_timestamps2[i] - peak_timestamps1[i])
        print(f"Offset is {peak_timestamps2[i] - peak_timestamps1[i]}")

    avg_offset /= len(peak_timestamps1)

    # return avg_offset, avg_drift
    return avg_offset

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
        # data_points = data_points[140000:180000]
        # data_points = data_points[50000:]
        data_points = data_points[80000:140000]

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

    # Error check
    if not timestamps:
        print("No data was successfully parsed. Cannot generate graph.")
        return

    # Variation and Decibels
    data_dict = {"Time": timestamps, "Voltage": voltages};
    df = pd.DataFrame(data_dict)
    df["Variation"] = df["Voltage"].rolling(window=500).var().rolling(window=1000).median()
    # df["Variation"] = df["Voltage"].rolling(window=500).var().rolling(window=1000).median()
    df["Decibels"] = df["Voltage"].rolling(window=500).apply(extract_decibels, raw=True)

    df["Variation_Normalized"] = (df["Variation"] - df["Variation"].min()) / (df["Variation"].max() - df["Variation"].min())

    return df

if __name__ == "__main__":
    # Ensure you have matplotlib installed: pip install matplotlib, also do pip install pandas, pip install numpy, pip install scipy

    '''
    UNCOMMENT LINES BELOW TO CHOOSE BETWEEN AUDIO AND PWM FILES
    NOTE: data_points = data_points[x:y] inside parse_file_to_dataframe DETERMINES RANGE OF POINTS TO GRAPH
    '''
    max_offset = 0.5

    dataframe1 = parse_file_to_dataframe("audio/panashe_audio1.txt")
    dataframe2 = parse_file_to_dataframe("audio/joshua_audio1.txt")
    # dataframe1 = parse_file_to_dataframe("pwm/panashe_pwm1.txt")
    # dataframe2 = parse_file_to_dataframe("pwm/joshua_pwm1.txt")

    # Finding peaks from normalized variation
    peaks_indices_filtered1, _ = find_peaks(dataframe1['Variation_Normalized'], prominence=0.05, distance=10)  # min 200 data points between peaks for now (about 0.2 sec), must be >= than max_offset
    peaks_indices_filtered2, _ = find_peaks(dataframe2['Variation_Normalized'], prominence=0.05, distance=10)  # need positive but small prominence so that local max instead of local min
    # peaks_indices_filtered1, _ = find_peaks(dataframe1['Variation_Normalized'], prominence=0.05)  # min 200 data points between peaks for now (about 0.2 sec), must be >= than max_offset
    # peaks_indices_filtered2, _ = find_peaks(dataframe2['Variation_Normalized'], prominence=0.05)  # need positive but small prominence so that local max instead of local min

    peak_timestamps1 = dataframe1['Time'].iloc[peaks_indices_filtered1].tolist()
    peak_values1 = dataframe1['Variation_Normalized'].iloc[peaks_indices_filtered1].tolist()
    peak_timestamps2 = dataframe2['Time'].iloc[peaks_indices_filtered2].tolist()
    peak_values2 = dataframe2['Variation_Normalized'].iloc[peaks_indices_filtered2].tolist()
    assert(len(peak_timestamps1) == len(peak_values1))
    assert(len(peak_timestamps2) == len(peak_values2))

    peak_timestamps1, peak_values1, peak_timestamps2, peak_values2 = match_peaks(peak_timestamps1, peak_values1, peak_timestamps2, peak_values2, max_offset)
    offset = calculate_offset(peak_timestamps1, peak_values1, peak_timestamps2, peak_values2)
    print("CALCULATED OFFSET IN SECONDS IS " + str(offset))

    # Graphing
    plt.figure(figsize=(10, 6))
    plt.plot(dataframe1["Time"].tolist(), dataframe1["Variation_Normalized"].tolist(), marker='o', linestyle='-', color='teal', markersize=8)
    plt.plot(dataframe2["Time"].tolist(), dataframe2["Variation_Normalized"].tolist(), marker='o', linestyle='-', color='red', markersize=8)
    
    plt.plot(peak_timestamps1, peak_values1, ".", color='purple', markersize=16, label='Peaks1')
    plt.plot(peak_timestamps2, peak_values2, ".", color='purple', markersize=16, label='Peaks2')

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


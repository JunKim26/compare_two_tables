# Title : Compare Two Tables
# Author: Jun Kim
# Date: 12/22/2021
# Description: In this program, a GUI will mimic the function of the compare tables in Ablebits. Once the program is run, a tkinter will be used to prompt a user to choose two CSV files. 
# One file will contain the primary keys and another column with values for commparison. The second value will contain the values we are comparing with the first CSV file. 
# The resulting output file will contain only the rows that had a matching value and save to a folder with a timestamp.


import pandas as pd                                                        
import os                                                                   
import tkinter as tk                                                       
from tkinter import *                                                    
from tkinter.filedialog import askopenfilename
from datetime import datetime                                             


window = tk.Tk()                                                            
window.geometry('200x200')                                                  

label = tk.Label(text='Compare Two Tables')                                     
label.pack()

def csv_opener():
    """ this function is used for the button to open the csv file """
    global csv_name
    global csv_file
    global csv_df
    
    # show an "Open" dialog box and return the path to the selected file
    csv_name = askopenfilename()                                            
    csv_file = open(csv_name, 'r')		   
    
    csv_data = pd.read_csv(csv_file) 
    csv_df = pd.DataFrame(csv_data)  

    return None


def comparison_opener():
    """ this function is used for the button to open the ids file """
    global ids_name
    global ids_file
    global ids_df
    

    ids_name = askopenfilename()
    ids_file = open(ids_name,'r')                                                                      
    ids_data = pd.read_csv(ids_file)
    ids_df = pd.DataFrame(ids_data)    

    end_button = Button(window, text = 'Create', command =window.destroy).pack()

    return None


# Main Function Section

def main():
    
    # Buttons that will show up on the tkinter window for user
    csv_button = Button(window, text = 'Open CSV File', command = csv_opener).pack() 
    ids_button = Button(window, text = 'Open Comparison File', command = comparison_opener).pack()

    window.mainloop()
    
    # year_month_day-hours_minutes_seconds_AM/PM ; used in Title    
    dt = datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')                                                                    

    input_file = os.path.basename(csv_name)
    file_name = str(dt) +" Matches from " + input_file                      

    script_dir = os.path.dirname(__file__)                                  
    rel_path = 'Output'
    
    # this joins the absolute path of current script with wanted relative path
    abs_file_path = os.path.join(script_dir, rel_path)                      

    comparison_values = []
    matched_IDs = []

    csv_second_column = csv_df.columns[1]
    
     # The name of the column that contains the comparison values
    for i in ids_df['Comparison Values']:                               
        comparison_values.append(i)
    
    # Primary ID 
    for i in range(len(csv_df['Key ID'])):                                     
        if csv_df[csv_second_column][i] in comparison_values:
            
            new_data = csv_df['Key ID'][i]
            matched_IDs.append(new_data)

    matched_IDs_df = pd.DataFrame(matched_IDs, columns=['Key ID'])
    matched_IDs_df[csv_second_column] = ''
    
    
    with open(abs_file_path+'/'+file_name, 'w',newline='') as new_file:	    
        
        # writes the dataframe into the new file without the indices
        matched_IDs_df.to_csv(new_file, index=False)                        

        csv_file.close()
        ids_file.close()

        
if __name__ == '__main__':
    main()


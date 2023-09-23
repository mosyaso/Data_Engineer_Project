import win32com.client as win32
import os
import pandas as pd
import tkinter as tk
from PIL import ImageTk, Image

def submit():
    folder_path = input_entry.get()
    path_label.config(text=f"Path:{folder_path}")
    email = input_email_entry.get()
    email_label.config(text=f"Email:{email}")
    
    def excel_to_pdf(excel_file, sheet_name, pdf_file):
        # Open Excel application
        excel_app = win32.Dispatch("Excel.Application")
        excel_app.Visible = False

        # Open the Excel file
        workbook = excel_app.Workbooks.Open(excel_file)

        try:
            # Select the specific sheet
            sheet = workbook.Sheets(sheet_name)

            # Save the sheet as PDF
            sheet.ExportAsFixedFormat(0, pdf_file)

        finally:
            # Close the workbook and quit Excel
            workbook.Close()
            excel_app.Quit()

    def excel_to_csv():
        # Specify the path to the Excel file
        excel_finance = r"{}\Solar_Billing.xlsx".format(folder_path)

        # Read the Excel file into a DataFrame
        df = pd.read_excel(excel_finance)

        # Specify the path to save the text file
        text_file = r"{}\Solar_Billing.csv".format(folder_path)

        # Convert DataFrame to text and save as a text file
        #df.to_csv(text_file, sep='\t', index=False, header=None)
        df.to_csv(text_file, index=False, header=None)

        #Set the rows to remove
        rows_to_remove = [12]
        df = df.drop(rows_to_remove)

        num_columns_to_remove = 7  # Specify the number of columns to remove
        df = df.iloc[:, :-num_columns_to_remove]

        df.to_csv(text_file, index=False, header=None)
        df = pd.read_csv(text_file, header=0)

        df['Month'] = pd.to_datetime(df['Month'])
        df['Month'] = df['Month'].dt.strftime('%d.%m.%Y')
        df['Amount_RM'] = df['Amount_RM'].apply(lambda x: "{:.2f}".format(float(x)))

        df.to_csv(text_file, index=False)

    def send_file_to_outlook():
        # Folder path containing the PDF and TXT files
        #folder_path = r"{}".format(folder_path)
        #folder_path = r"C:\Users\syakir1937\Task Scheduler\Solar Billing\Billing Database"

        # Create an Outlook application object
        outlook = win32.Dispatch("Outlook.Application")

        # Get the Namespace and create a new MailItem
        namespace = outlook.GetNamespace("MAPI")
        mail_item = outlook.CreateItem(0)

        # Set the email properties
        mail_item.Subject = "Invoice Solar Billing"
        mail_item.Body = "Please find the attached files."

        # Loop through the files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
        
            # Check if the file is a PDF or csv file
            if file_name.lower().endswith((".pdf", ".csv")):
                # Add the file as an attachment
                attachment = mail_item.Attachments.Add(Source=file_path)
                attachment.DisplayName = file_name

        # Set the recipient email address
        mail_item.To = email

        # Send the email
        mail_item.Send()

    workbooks = [
        {'input_path': r"{}\Customer1.xlsx".format(folder_path), 'output_path': r"{}\Customer1.pdf".format(folder_path), 'sheet_names': "Customer1 Template"},
        {'input_path': r"{}\Customer2.xlsx".format(folder_path), 'output_path': r"{}\Customer2.pdf".format(folder_path), 'sheet_names': "Customer2 Template"},
        {'input_path': r"{}\Customer3.xlsx".format(folder_path), 'output_path': r"{}\Customer3.pdf".format(folder_path), 'sheet_names': "Customer3 Template"},
    ]

    # Loop through each workbook and convert sheets to PDF
    for workbook in workbooks:
        excel_file = workbook['input_path']
        pdf_file = workbook['output_path']
        sheet_name = workbook['sheet_names']

        excel_to_pdf(excel_file, sheet_name, pdf_file)    
        excel_to_csv()

    send_file_to_outlook()

# Create the tkinter window
window = tk.Tk()
window.title("Solar Bill Invoice Generator")
window.geometry("450x350")

current_path = os.getcwd()

# Load the image file from disk.
#icon = tk.PhotoImage(file=r"{}\malakoff-icon.png".format(current_path))
icon = tk.PhotoImage(file=r"C:\Users\syakir1937\Task Scheduler\Solar Billing\malakoff-icon.png".format(current_path))
window.iconphoto(True, icon)

# Load and display the logo
# logo_image = Image.open(r"{}\malakoff_mmc_logo-removebg-preview.png".format(current_path))
logo_image = Image.open(r"C:\Users\syakir1937\Task Scheduler\Solar Billing\malakoff_mmc_logo-removebg-preview.png".format(current_path))
#logo_image = logo_image.resize((300, 150))
logo_image = logo_image.resize((290, 100))
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(window, image=logo_photo)
logo_label.pack(pady=20)

# Create and display the welcome label
welcome_label = tk.Label(window, text="Welcome!", font=("Helvetica", 16))
welcome_label.pack(pady=5)

path_label = tk.Label(window, text="Target Path", font=("Helvetica", 10))
path_label.pack(pady=0)

# Create and display the input field
input_entry = tk.Entry(window, width=45)
input_entry.pack(pady=5)

email_label = tk.Label(window, text="Email", font=("Helvetica", 10))
email_label.pack(pady=0)

# Create and display the input field
input_email_entry = tk.Entry(window, width=40)
input_email_entry.pack(pady=10)

# Create and display the submit button
submit_button = tk.Button(window, text="Submit", command=submit)
submit_button.pack()

# Start the tkinter event loop
window.mainloop()

#folder_path = r'C:\Users\syakir1937\Documents\Solar Billing\Billing Database'
# folder_path = input("Enter Dir Path: ")
# folder_path = str(folder_path)

# email = input("Enter Recipient Email: ")
# email = str(email)

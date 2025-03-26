import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Function to create a database
def create_database():
    conn = sqlite3.connect('jio_sim_database.db')
    c = conn.cursor()
    
    # Create table to store SIM number details
    c.execute('''CREATE TABLE IF NOT EXISTS sim_numbers
                 (id INTEGER PRIMARY KEY, sim_number TEXT, date TEXT)''')
    
    conn.commit()
    conn.close()

# Function to generate a random Jio SIM number (starting with 700 or 701)
def generate_sim_number():
    # Jio numbers generally start with 700, 701, etc.
    prefix = random.choice([700, 701, 702, 703, 704])
    sim_number = f"{prefix}{random.randint(1000000, 9999999)}"
    return sim_number

# Function to store the generated SIM number in the database
def store_sim_number(sim_number):
    conn = sqlite3.connect('jio_sim_database.db')
    c = conn.cursor()
    
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    c.execute('''INSERT INTO sim_numbers (sim_number, date)
                 VALUES (?, ?)''', (sim_number, date))
    
    conn.commit()
    conn.close()

# Function to send the SIM number via email
def send_email(to_email, sim_number):
    from_email = "your_email@gmail.com"  # Replace with your email
    password = "your_password"  # Replace with your email password

    subject = "Your New Jio SIM Number"
    body = f"Your new Jio SIM number is: {sim_number}\n\nThank you for using our service!"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("SIM number sent successfully via email!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function to interact with the user
def main():
    create_database()  # Create the database and table if not already created
    
    while True:
        print("\n1. Generate Jio SIM Number\n2. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Generate a new Jio SIM number
            sim_number = generate_sim_number()
            print(f"Generated SIM Number: {sim_number}")
            
            # Store the generated SIM number in the database
            store_sim_number(sim_number)
            
            # Ask the user for the email address to send the SIM number
            email = input("Enter the email address to send the SIM number: ")
            
            # Send the SIM number via email
            send_email(email, sim_number)
        
        elif choice == "2":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
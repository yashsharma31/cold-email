import pandas as pd

# Read the CSV file
df = pd.read_csv('dummy_data.csv')

# Update all email addresses to retrostrikewhy@gmail.com
df['email'] = 'retrostrikewhy@gmail.com'

# Save the updated data back to the CSV file
df.to_csv('dummy_data.csv', index=False)

print("All email addresses have been updated to retrostrikewhy@gmail.com") 
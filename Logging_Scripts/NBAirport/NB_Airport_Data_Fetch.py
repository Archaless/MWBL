from datetime import datetime
import requests
import sys
import os

# Will automatically pull New Bedford Aitport Meteorlogical data from https://www.ncei.noaa.gov/oa/local-climatological-data/v2/access/
# Should be added to user MWBL's crontab: 

def NB_Airport_Data_Fetch(year = str(datetime.now().year), token = 'pEhotRAaEElMkRBtJcIFwUQdfwCAMObh'):
    # "year" is an optional argument, default will download current year
    try:
        url = 'https://www.ncei.noaa.gov/oa/local-climatological-data/v2/access/' + year + '/LCD_USW00094726_' + year + '.csv'
        # Overwrite old file everytime, data can only be selected for a desired year from NOAA website
        save_path = '/usr2/MWBL/Data/NBAirport/raw/NB_Airport_' + year + '.csv'
        # Send HTTP GET request to the URL
        response = requests.get(url, headers = {'Token': token}, stream=True)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Download and write the file in chunks
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f'Download completed: {save_path}')
    except requests.exceptions.RequestException as e:
        print(f'Error downloading file: {e}')
    except Exception as e:
        print(f'General error: {e}')

# Main function to parse year argument and run function above
if __name__ == '__main__':
    if len(sys.argv) > 3:
        print('ERROR - Usage: python NB_Airport_Data_Fetch.py <year> <token>(optional)')
        print('Received: ')
        for stuff in sys.argv:
            print(stuff)
        sys.exit(1)
    if len(sys.argv) == 1:
        NB_Airport_Data_Fetch()
    elif len(sys.argv) == 2:
        year = sys.argv[1]
        NB_Airport_Data_Fetch(year)
    else:
        year = sys.argv[1]
        token = sys.argv[2]
        NB_Airport_Data_Fetch(year)


# Example usage:
# python NB_Airport_Data_Fetch.py 2026 pEhotRAaEElMkRBtJcIFwUQdfwCAMObh
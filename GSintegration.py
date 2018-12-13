from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
data_source = '1qZg9dfwO4DU3rg0FTEQhhWdNEHmKycUk8fDgjUOhZxk'
data_range = 'Crowdfunding Q!A2:H'

# """Shows basic usage of the Sheets API.
# Prints values from a sample spreadsheet.
# """
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
store = file.Storage('token.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
sheet = service.spreadsheets()

result = sheet.values().get(spreadsheetId=data_source, range=data_range).execute()
values = result.get('values', [])

def q_n_bg(values):
    bg_color_palette = {'blue': [], 'white': [], 'orange': [], 'green': [], 'purple': [], 'black': [], 'red': [], 'darkred': []}

    # THIS IS WORKING BUT NOT GOOD :)
    # if not values:
    #     print('No data found.')
    # else:
    #     print('++++++++++++++++All The Room Questions:')
    #     for row in values:
    #         if row[0]:
    #             bg_color_palette['blue'].append(row[0])
    #             if row[1]:
    #                 bg_color_palette['white'].append(row[1])
    #                 print(bg_color_palette['white'])
    #                 if row[2]:
    #                     bg_color_palette['orange'].append(row[2])
    #                     if row[3]:
    #                         bg_color_palette['green'].append(row[3])
    #                         if row[4]:
    #                             bg_color_palette['purple'].append(row[4])
    #                             if row[5]:
    #                                 bg_color_palette['black'].append(row[5])
    #                                 if row[6]:
    #                                     bg_color_palette['red'].append(row[6])

    # print(bg_color_palette['blue'])

    # Print columns A and E, which correspond to indices 0 and 4.
    # print('%s, %s' % (row[0], row[4]))
    # print(len(row), row)

    # print(values)

    if not values:
        print("No Data Found")
    else:
        for row in values:

            for q in range(len(row)):
                if q != '':
                    if q == 0:
                        bg_color_palette['blue'].append(row[q])
                    if q == 1:
                        bg_color_palette['white'].append(row[q])
                    if q == 2:
                        bg_color_palette['orange'].append(row[q])
                    if q == 3:
                        bg_color_palette['green'].append(row[q])
                    if q == 4:
                        bg_color_palette['purple'].append(row[q])
                    if q == 5:
                        bg_color_palette['black'].append(row[q])
                    if q == 6:
                        bg_color_palette['red'].append(row[q])
                    if q == 7:
                        bg_color_palette['darkred'].append(row[q])
    pprint(bg_color_palette)

    return bg_color_palette
    # pprint(bg_color_palette.values)


def main():
    return q_n_bg(values)


if __name__ == '__main__':
    main()
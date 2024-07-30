import json
import sqlite3

conn = sqlite3.connect('caps.db')
cursor = conn.cursor()
count=1
try:
    with open('5json.json', 'r') as json_file:
        data = json.load(json_file)
        if isinstance(data, list):
            for packet in data:
                frame = packet['_source']['layers']['frame']
                wlan_radio = packet['_source']['layers']['wlan_radio']
                wlan = packet['_source']['layers']['wlan']
                
                if frame['frame.protocols'].startswith('radiotap:wlan_radio:wlan'):
                    print('radiotap:wlan_radio:wlan data found\n')
                    print('Count:' + str(count) )
                    print(json.dumps(wlan, indent=2))

                    # Extract the necessary data
                    wlan_radio_channel = wlan_radio.get('wlan_radio.channel')
                    wlan_radio_signal_dbm = wlan_radio.get('wlan_radio.signal_dbm')
                    wlan_ta = wlan.get('wlan.ta')
                    wlan_da = wlan.get('wlan.da')
                    wlan_ra = wlan.get('wlan.ra')  
                    wlan_bssid = wlan.get('wlan.bssid')
                    wlan_ta_resolved = wlan.get('wlan.ta_resolved')
                    wlan_da_resolved = wlan.get('wlan.da_resolved')
                    wlan_ra_resolved = wlan.get('wlan.ra_resolved')  
                    wlan_bssid_resolved = wlan.get('wlan.bssid_resolved')
                    frame_time = frame.get('frame.time')
                    frame_time_epoch = frame.get('frame.time_epoch')
                    
                    # INSERT ALL PACKAGE DATA TO WLAN TABLE
                    insert_wlan_sql = '''INSERT INTO wlan (wlan_radio_channel, wlan_radio_signal_dbm, wlan_ta, wlan_da, wlan_ra, wlan_bssid, wlan_ta_resolved, wlan_da_resolved, wlan_ra_resolved, wlan_bssid_resolved, frame_time, frame_time_epoch)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                    data_tuple = (wlan_radio_channel, wlan_radio_signal_dbm, wlan_ta, wlan_da, wlan_ra, wlan_bssid, wlan_ta_resolved, wlan_da_resolved, wlan_ra_resolved, wlan_bssid_resolved, frame_time, frame_time_epoch)
                    cursor.execute(insert_wlan_sql, data_tuple)


                    # INSERT ONLY UNIQUE VALUES TO MAC TABLE
                    if wlan_ta is not None:
                        insert_stmt = '''INSERT OR IGNORE INTO mac (mac_id, first_seen, mac_resolved)
                                        VALUES (?, ?, ?)'''
                        data_tuple = (wlan_ta, frame_time, wlan_ta_resolved)
                        cursor.execute(insert_stmt, data_tuple)

                    if wlan_da is not None:
                        insert_stmt = '''INSERT OR IGNORE INTO mac (mac_id, first_seen, mac_resolved)
                                        VALUES (?, ?, ?)'''
                        data_tuple = (wlan_da, frame_time, wlan_da_resolved)
                        cursor.execute(insert_stmt, data_tuple)

                    if wlan_ra is not None:
                        insert_stmt = '''INSERT OR IGNORE INTO mac (mac_id, first_seen, mac_resolved)
                                        VALUES (?, ?, ?)'''
                        data_tuple = (wlan_ra, frame_time, wlan_ra_resolved)
                        cursor.execute(insert_stmt, data_tuple)

                    # INSERT ONLY UNIQUE VALUES TO talkingto TABLE
                    if wlan_ta is not None and wlan_ra is not None:
                        insert_stmt = '''INSERT OR IGNORE INTO talkingto (mac_sender, mac_receiver, mac_sender_resolved, mac_receiver_resolved, first_talked)
                                        VALUES (?, ?, ?, ?, ?)'''
                        data_tuple = (wlan_ta, wlan_ra, wlan_ta_resolved, wlan_ra_resolved, frame_time)
                        cursor.execute(insert_stmt, data_tuple)

                    count += 1
                else:
                    print('frame.protocols is not radiotap:wlan_radio:wlan')
        else:
            print('The JSON file does not contain an array (list).')

    # Commit the changes
    conn.commit()

except FileNotFoundError as e:
    print(f'The file was not found: {e}')
except json.JSONDecodeError as e:
    print(f'Error decoding JSON: {e}')
except Exception as e:
    print(f'An error occurred: {e}')

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()

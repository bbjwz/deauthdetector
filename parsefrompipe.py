import sys
import json
import sqlite3

print('Lets GO!')

try:
    for line in sys.stdin:
        try:
            packet = json.loads(line)
            
            if 'layers' in packet:
                #print(json.dumps(packet, indent=2))
                
                frame = packet['layers']['frame']
                wlan_radio = packet['layers']['wlan_radio']
                wlan = packet['layers']['wlan']
            
                # Further check for the 'frame.protocols' key
                if frame['frame_frame_protocols'].startswith('radiotap:wlan_radio:wlan'):
                    conn = sqlite3.connect('caps.db')
                    cursor = conn.cursor()
                    #print('radiotap:wlan_radio:wlan data found')
                    #print(json.dumps(frame, indent=2))
                    
                    # Extract the necessary data
                    wlan_radio_channel = wlan_radio.get('wlan_radio_wlan_radio_channel')
                    wlan_radio_signal_dbm = wlan_radio.get('wlan_radio_wlan_radio_signal_dbm')
                    
                    wlan_ta = wlan.get('wlan_wlan_ta')
                    wlan_da = wlan.get('wlan_wlan_da')
                    wlan_ra = wlan.get('wlan_wlan_ra')  
                    wlan_bssid = wlan.get('wlan_wlan_bssid')
                    wlan_ta_resolved = wlan.get('wlan_wlan_ta_resolved')
                    wlan_da_resolved = wlan.get('wlan_wlan_da_resolved')
                    wlan_ra_resolved = wlan.get('wlan_wlan_ra_resolved')  
                    wlan_bssid_resolved = wlan.get('wlan_wlan_bssid_resolved')
                    frame_time = frame.get('frame_frame_time')
                    frame_time_epoch = frame.get('frame_frame_time_epoch')

                    '''
                    print(f"WLAN Radio Channel: {wlan_radio_channel}")
                    print(f"WLAN Radio Signal dBm: {wlan_radio_signal_dbm}")
                    print(f"WLAN Transmitter Address (TA): {wlan_ta}")
                    print(f"WLAN Destination Address (DA): {wlan_da}")
                    print(f"WLAN Receiver Address (RA): {wlan_ra}")
                    print(f"WLAN Basic Service Set Identifier (BSSID): {wlan_bssid}")
                    print(f"WLAN TA Resolved: {wlan_ta_resolved}")
                    print(f"WLAN DA Resolved: {wlan_da_resolved}")
                    print(f"WLAN RA Resolved: {wlan_ra_resolved}")
                    print(f"WLAN BSSID Resolved: {wlan_bssid_resolved}")
                    print(f"Frame Time: {frame_time}")
                    print(f"Frame Time Epoch: {frame_time_epoch}")
                    '''


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
                        insert_stmt = '''INSERT OR IGNORE INTO talkingto (mac_sender, mac_receiver, mac_sender_resolved, mac_receiver_resolved, wlan_radio_channel, wlan_radio_signal_dbm, first_talked)
                                        VALUES (?, ?, ?, ?, ?, ?, ?)'''
                        data_tuple = (wlan_ta, wlan_ra, wlan_ta_resolved, wlan_ra_resolved, wlan_radio_channel, wlan_radio_signal_dbm, frame_time)
                        cursor.execute(insert_stmt, data_tuple)

                    # Commit the changes
                    conn.commit()
                      # Close the cursor and connection
                    cursor.close()
                    conn.close()
                    
                else:
                    print('radiotap:wlan_radio missing')
                
        except json.JSONDecodeError:
            continue  # Handle incomplete or malformed JSON
except Exception as e:
    print(f'Foutmelding: {e}')

finally:
  print('Done')












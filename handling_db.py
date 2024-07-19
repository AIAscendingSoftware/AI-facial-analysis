

import mysql.connector

def insert_video_details(data):
    conn = None
    cursor = None
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(
            host="89.116.230.242",
            user="elude_pro_communication",
            password="Elude@pro321^",
            database="elude_pro_communication"
        )

        # Create a cursor object
        cursor = conn.cursor()

        # Define the SQL query to insert data
        sql = "INSERT INTO elude_pro_communication.pro_communication_ai_face_video_model (base_url, byte_size, date_and_time, user_id, video_category, video_name, video_type) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        # Execute the SQL command
        cursor.execute(sql, data)

        # Commit the changes to the database
        conn.commit()

        # Retrieve the last inserted ID
        last_id = cursor.lastrowid

        return {"message": "Data inserted successfully for insert_video_details", "id": last_id}

    except mysql.connector.Error as error:
        return {"error": f"Failed to insert data into MySQL table: {error}"}

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("MySQL connection is closed for insert_video_details")


def insert_video_scores(data):
    conn = None
    cursor = None
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(
            host="89.116.230.242",
            user="elude_pro_communication",
            password="Elude@pro321^",
            database="elude_pro_communication"
        )

        # Create a cursor objectS
        cursor = conn.cursor()

        # Define the SQL query to insert data
        sql = "INSERT INTO elude_pro_communication.pro_communication_ai_face_details_model (angry, arms_crossed, body_language_score, communication_score, disgust, eye_contact, face_confidence, fcial_score, fear, fluency, grammar, hand_usage, happy, leg_movement, looking_straight, nautral, over_all_scroe, pronunciation, sad, smile_count, speech_rate, speech_score, surprise, tone, user_id, video_id, voice_confidence, voice_graph_base64, weight_balanced_on_both_legs, weight_on_one_leg, wrists_closed) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # Execute the SQL command
        cursor.execute(sql, data)

        # Commit the changes to the database
        conn.commit()


        return {"message": "Data inserted successfully for insert_video_scores"}

    except mysql.connector.Error as error:
        return {"error": f"Failed to insert data into MySQL table: {error}"}

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("MySQL connection is closed for insert_video_scores")



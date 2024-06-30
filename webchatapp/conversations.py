import sqlite3
import os
import json

class EventFetcher:

    @staticmethod
    def fetch_text_by_event():
        try:
            os.chdir("/home/timesys/AdmissionChatbot")
            conn = sqlite3.connect("admiss.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM events;")
            rows = cursor.fetchall()

            user_messages = []
            bot_messages = []
            for row in rows:
                # Extracting the JSON data from the tuple
                json_data = row[-1]

                # Parse the JSON data
                data = json.loads(json_data)

                # Check if the event is "user"
                if data['event'] == 'user':
                    # Print the text data
                    user_message = data.get('text', 'Text not available')
                    user_messages.append(user_message)

                # Check if the event is "bot"
                if data['event'] == 'bot':
                    # Print the text data
                    bot_message = data.get('text', 'Text not available')
                    user_messages.append(bot_message)

            conn.close()
            return user_messages
        except Exception as e:
            print("Error:", e)
            return []

# if __name__ == "__main__":
#     EventFetcher.fetch_text_by_event()

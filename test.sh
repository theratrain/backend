#!/bin/bash

# API base URL
API_URL="http://localhost:8000"

# Create a new user
echo "Creating new user..."
USER_RESPONSE=$(curl -s -X POST "$API_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "alias": "test_user2",
    "is_ai": false,
    "config": {
      "system_prompt": "Du bist ein Teenager mit Depressionen. Du sprichst mit einem Therapeuten. Antworte immer in deutscher Sprache. Antworte realistisch und passend zu deiner Persona.",
      "model": "llama-3.2-90b-text-preview"
    }
  }')

# Check if user creation was successful
if [[ $(echo $USER_RESPONSE | jq -r '.id' 2>/dev/null) == "null" ]]; then
    echo "Error creating user:"
    echo $USER_RESPONSE | jq '.'
    exit 1
fi

USER_ID=$(echo $USER_RESPONSE | jq -r '.id')
echo "Created user with ID: $USER_ID"


# Create a new session
echo -e "\nCreating new session..."
echo "Calling URL: $API_URL/chat/new/$USER_ID"
SESSION_RESPONSE=$(curl -s -X POST "$API_URL/chat/new/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hallo, wie geht es dir?"
  }')

# Check if session creation was successful by checking if session_id exists and is not null
if [[ $(echo $SESSION_RESPONSE | jq 'has("session_id")') == "true" && $(echo $SESSION_RESPONSE | jq -r '.session_id') != "null" ]]; then
    SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')
    echo "Created session with ID: $SESSION_ID"
    echo "Response:"
    echo $SESSION_RESPONSE | jq '.'
else
    echo "Error creating session:"
    echo $SESSION_RESPONSE | jq '.'
    exit 1
fi

# Test chat endpoint
echo -e "\nTesting chat..."
CHAT_RESPONSE=$(curl -s -X POST "$API_URL/chat/$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hallo, wie geht es dir?"
  }')

echo "Chat response:"
echo $CHAT_RESPONSE | jq '.'
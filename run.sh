# Run the TTS server first and wait until it prints "Server ready"
TTS_SERVER="./TTS_Really_m/server.py"
if [ -f "$TTS_SERVER" ]; then
    echo "Starting the TTS server..."
    python3 "$TTS_SERVER" | tee server_output.log &
    # Wait until "Server ready" is printed
    while ! grep -q "Server ready" server_output.log; do
        sleep 1
    done
    echo "TTS server is ready."
else
    echo "$TTS_SERVER not found. Skipping."
fi

# Run the main Python script after the server is ready
MAIN_SCRIPT="main.py"
if [ -f "$MAIN_SCRIPT" ]; then
    echo "Running $MAIN_SCRIPT..."
    python3 "$MAIN_SCRIPT" &
else
    echo "$MAIN_SCRIPT not found. Skipping."
fi

echo "Setup and execution complete."

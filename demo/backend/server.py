import json
import os
import sys
sys.path.append('../../')

import asyncio
import time

from fastapi import FastAPI, WebSocket

app = FastAPI()

# Gets root directory by moving two directories up from the working directory.
root_dir = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))

# Define a WebSocket endpoint at the path `/ws`.
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Send an acknowledgement to the client.
    await websocket.accept()

    try:
        # Receive the Python code from the client.
        source_code = await websocket.receive_text()

        # Start a new subprocess to execute the code.
        proc = await asyncio.create_subprocess_exec(
            "python", "pyc", "-c", source_code,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,  # Redirect stderr to stdout
            cwd=root_dir
        )

        # Create a buffer to store the output from the subprocess.
        stdout_buffer = []

        # Create a list to keep track of when the output buffer was last updated.
        prev_updated = [time.perf_counter()]

        # Define a coroutine to check if it's time to send output to the client.
        async def check_time():
            # Wait until 0.1 seconds have elapsed since the output buffer was last updated,
            # or until there is new output to send.
            while time.perf_counter() - prev_updated[0] < 0.1 or len(stdout_buffer) == 0:
                await asyncio.sleep(0.02)
            # Update the time when the output buffer was last updated.
            prev_updated[0] = time.perf_counter()
            return True
        
        # Start coroutines to read from the subprocess stdout, receive messages from the client,
        # and check if it's time to send output to the client.
        stdout_task = asyncio.create_task(proc.stdout.read(1))
        websocket_task = asyncio.create_task(websocket.receive_text())
        output_task = asyncio.create_task(check_time())

        # Loop until the subprocess is finished.
        while True:
            if proc.returncode is not None:
                # If the subprocess has finished, send the remaining output to the client,
                # along with the return code, and close the WebSocket connection.
                stdout_buffer.extend(list(map(chr, await proc.stdout.read()))) 
                await websocket.send_text(json.dumps({"output": "".join(stdout_buffer)}))
                stdout_buffer.clear()
                await websocket.send_text(json.dumps({"output": f"\nProcess finished with return code: {proc.returncode}"}))
                await websocket.close()
                break

            # Wait until one of the coroutines has finished.
            done, _ = await asyncio.wait(
                [stdout_task, websocket_task, output_task],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # If the stdout coroutine has finished, read the output and add it to the buffer.
            if stdout_task in done:
                data = await stdout_task
                if data:
                    stdout_buffer.extend(data.decode())
                stdout_task.cancel()
                stdout_task = asyncio.create_task(proc.stdout.read(1))

            # If the client has sent a message, send it to the subprocess stdin.
            if websocket_task in done:
                message = await websocket_task
                proc.stdin.write(message.encode())
                await proc.stdin.drain()
                websocket_task.cancel()
                websocket_task = asyncio.create_task(websocket.receive_text())

            # If it's time to send output to the client, send the current buffer contents.
            if output_task in done:
                await output_task
                await websocket.send_text(json.dumps({"output": "".join(stdout_buffer)}))
                stdout_buffer.clear()
                output_task.cancel()
                output_task = asyncio.create_task(check_time())

    except Exception as e:
        # If an error occurs, send the error message to the client and close the WebSocket connection.
        if proc is not None and proc.returncode is None:
            proc.kill()
        await websocket.send_text(json.dumps({"output": f"\nError: {e}"}))
        await websocket.close()

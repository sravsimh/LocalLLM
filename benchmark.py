import subprocess
import json
import time


def run_and_store_final_response(command):
    try:
        # Run the command
        start_time = time.time()
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)
        end_time = time.time()
        jsonvalue = json.loads(result.stdout.split('\n')[-2])
        jsonvalue.pop('context', None)

        try:
            # Write the output to a file
            with open('final_response.json', 'w') as f:
                json.dump({"response": jsonvalue}, f, indent=4)

            total_duration = (jsonvalue['total_duration'])/1e9
            load_duration = (jsonvalue['load_duration'])/1e9
            prompt_eval_duration = (jsonvalue['prompt_eval_duration'])/1e9
            eval_duration = (jsonvalue['eval_duration'])/1e9
            prompt_count = jsonvalue['prompt_eval_count']
            eval_count = jsonvalue['eval_count']
            total_tokens = prompt_count + eval_count
            tpm = total_tokens / eval_duration if eval_duration > 0 else 0
            latency = end_time - start_time

            print(f"Total Duration: {total_duration:.2f} seconds,load_duration: {load_duration:.2f} seconds, prompt_eval_duration: {prompt_eval_duration:.2f} seconds, eval_duration: {eval_duration:.2f} seconds, prompt_count: {prompt_count}, eval_count: {eval_count}, total_tokens: {total_tokens}, tpm: {tpm:.2f}, latency: {latency:.2f} seconds,")

        except IOError as io_error:
            print("🚨 Error writing to file:", io_error)
    except Exception as e:
        print("🚨 Error running command:", e)


# Example command (replace with your actual curl or API call)
cmd = (
    'curl http://127.0.0.1:11434/api/generate '
    '-H "Content-Type: application/json" '
    '-d "{\\"model\\": \\"llama3.1\\", \\"prompt\\": \\"What is AI?\\"}"'
)

run_and_store_final_response(cmd)

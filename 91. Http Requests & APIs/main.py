"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from pypdf import PdfReader

# Create a client using the credentials and region defined in the AWS profile.
profile_name = os.getenv("AWS_PROFILE")
region_name = os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION") or "us-east-1"

session_kwargs = {"region_name": region_name}
if profile_name:
    session_kwargs["profile_name"] = profile_name

try:
    session = Session(**session_kwargs)
except ProfileNotFound:
    print(
        f"El perfil de AWS '{profile_name}' no existe. "
        f"Configúralo con 'aws configure --profile {profile_name}' o define tus credenciales por defecto."
    )
    sys.exit(1)

polly = session.client("polly")

try:
    reader = PdfReader("./guerra.pdf")
    responses = []
    for page in reader.pages:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=page.extract_text(), OutputFormat="mp3", VoiceId="Mia", LanguageCode="es-MX")
        responses.append(response)
except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
output = os.path.join(gettempdir(), "speech.mp3")
for response in responses:
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb" if response == responses[0] else "ab") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

# Play the audio using the platform's default player
if sys.platform == "win32":
    os.startfile(output)
else:
    # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, output])
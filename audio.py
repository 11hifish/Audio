import pyaudio
import wave
import dropbox

# Codes for getting info about input devices:
# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
# for i in range (0,numdevices):
#     if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
#         print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
#  
#     if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
#         print ("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
# print("default input device:",p.get_default_input_device_info())
# devinfo = p.get_device_info_by_index(2)
# print ("Selected device is ",devinfo.get('name'))
# if p.is_format_supported(44100.0,  # Sample rate
#                          input_device=devinfo["index"],
#                          input_channels=devinfo['maxInputChannels'],
#                          input_format=pyaudio.paInt16):
#   print ('Supports!!!')
# p.terminate()

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file_new.mp3"
  
audio = pyaudio.PyAudio()
   
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS, input_device_index = 2,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")
frames = []
   
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")
  
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
   
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
  
# upload the file to dropbox:
# Please replace <My_App_Key>, <My_App_Secret> and 
# <My_Dropbox_Access_Token> with actual values.
app_key = '<My_App_Key>'
app_secret = '<My_App_Secret>'
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()
  
access_token = "<My_Dropbox_Access_Token>" 
client = dropbox.client.DropboxClient(access_token)
  
print ('linked account: ')
print (client.account_info())
   
f = open('file_new.mp3', 'rb')
response = client.put_file('/file_new.mp3', f)
print ("uploaded:")
print (response)
   
folder_metadata = client.metadata('/')
print ('metadata: ')
print (folder_metadata)
   
f, metadata = client.get_file_and_metadata('/file_new.mp3')
out = open('file_new.mp3', 'wb')
out.write(f.read())
out.close()
print (metadata)

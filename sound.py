from pydub import AudioSegment
import os


def sound_playback(weather_data):
    print(weather_data)

    # Want to get hourly temperature and wind speed data for the next 8 units only.
    temperatures = weather_data[0][0:8]
    wind_speed = weather_data[1][0:8]

    print(temperatures)
    print(wind_speed)

    modify_sound(temperatures, wind_speed)


def modify_sound(temperatures, wind_speed):
    beep_sound = AudioSegment.from_wav('beep.wav')
    wind_sound_effect = AudioSegment.from_wav('wind.wav')

    temperature_sound = []
    for temperature in temperatures:
        temperature_sound.append(speed_change(beep_sound, temperature))

    new_sound = []
    for sound in temperature_sound:
        sound = sound.fade_in(500).fade_out(500)

        i = 1
        while len(sound) < 5000:
            sound = sound * i
            i += 1
        i = 1
        # Make sure only 5 seconds and not more
        sound = sound[:5000]

        new_sound.append(sound)
        # print(len(sound))
        # play(sound)

    wind_sound = []
    for speed in wind_speed:
        wind_sound.append(volume_change(wind_sound_effect, speed).fade_in(200).fade_out(200))



    mixed_sounds = []
    for temp_sound, wind_sound in zip(new_sound, wind_sound):
        mixed_sounds.append(temp_sound.overlay(wind_sound))

    silent_sound = (wind_sound_effect - 100)[:5000]


    channel1 = mixed_sounds[0]
    channel2 = mixed_sounds[1]
    channel3 = mixed_sounds[2]
    channel4 = mixed_sounds[3]
    channel5 = mixed_sounds[4]
    channel6 = mixed_sounds[5]
    channel7 = mixed_sounds[6]
    channel8 = mixed_sounds[7]

    multi_audio1 = AudioSegment.from_mono_audiosegments(channel1, silent_sound, silent_sound, silent_sound,
                                                        silent_sound, silent_sound, silent_sound, silent_sound)
    multi_audio2 = AudioSegment.from_mono_audiosegments(silent_sound, channel2, silent_sound, silent_sound,
                                                        silent_sound, silent_sound, silent_sound, silent_sound)
    multi_audio3 = AudioSegment.from_mono_audiosegments(silent_sound, silent_sound, channel3, silent_sound,
                                                        silent_sound, silent_sound, silent_sound, silent_sound)
    multi_audio4 = AudioSegment.from_mono_audiosegments(silent_sound, silent_sound, silent_sound, channel4,
                                                        silent_sound, silent_sound, silent_sound, silent_sound)
    multi_audio5 = AudioSegment.from_mono_audiosegments(silent_sound, silent_sound, silent_sound, silent_sound,
                                                        channel5, silent_sound, silent_sound, silent_sound)
    multi_audio6 = AudioSegment.from_mono_audiosegments(silent_sound, silent_sound, silent_sound, silent_sound,
                                                        silent_sound, channel6, silent_sound, silent_sound)
    multi_audio7 = AudioSegment.from_mono_audiosegments(silent_sound, silent_sound, silent_sound, silent_sound,
                                                        silent_sound, silent_sound, channel7, silent_sound)
    multi_audio8 = AudioSegment.from_mono_audiosegments(silent_sound, silent_sound, silent_sound, silent_sound,
                                                        silent_sound, silent_sound, silent_sound, channel8)

    final_sound = multi_audio1 + multi_audio2 + multi_audio3 + multi_audio4 + multi_audio5 + multi_audio6 + multi_audio7 + multi_audio8

    final_sound.export("final.wav", format="wav")

    os.startfile("final.wav")


def volume_change(sound, wind_speed):
    return sound + (wind_speed * 0.3)


def speed_change(sound, temperature):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second

    speed = float(1 - (temperature * 0.02))

    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

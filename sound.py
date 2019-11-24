from pydub import AudioSegment, effects
from pydub.playback import play
import simpleaudio as sa


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

    # for sound in wind_sound:
    #     # sound.fade_in(200).fade_out(200)
    #     # play(sound)

    mixed_sounds = []
    for temp_sound, wind_sound in zip(new_sound, wind_sound):
        # play(temp_sound)
        # play(wind_sound)
        mixed_sounds.append(temp_sound.overlay(wind_sound))

    # for sounds in mixed_sounds:
    #     play(sounds.fade_in(200).fade_out(200))

    silent_sound = (wind_sound_effect - 100)[:5000]

    print(mixed_sounds[0].frame_count())
    print(silent_sound.frame_count())

    channel1 = mixed_sounds[0]
    channel2 = mixed_sounds[7]

    stereo_sound1 = AudioSegment.from_mono_audiosegments(silent_sound, channel2)
    stereo_sound2 = AudioSegment.from_mono_audiosegments(channel1, silent_sound)
    play(stereo_sound1)
    play(stereo_sound2)
    # stereo_sound.export("test.wav", format="wav")




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

#
# slow_sound = speed_change(sound, 0.75)
# fast_sound = speed_change(sound, 2.0)
# # chipmunk_sound = pitch_change(sound)
#
# print(len(sound))
# # print(len(chipmunk_sound))
#
# chipmunk_sound = speed_change(sound, 0.40)
# # chipmunk_sound = pitch_change(sound, 0.5 / 12)
#
#
# print(len(chipmunk_sound))
#
# # chipmunk_sound = effects.normalize(chipmunk_sound)
#
# play(chipmunk_sound.fade_in(500).fade_out(500) * 5)

# sound = AudioSegment.from_file('wind.wav')
#
# play(sound.fade_in(200).fade_out(200) + 15)

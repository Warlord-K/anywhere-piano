from Instrument.Instrument import *

class Piano:
    
    def __init__(self):
        self.piano = Instrument(bit_rate = 44100)

        # 5th Octave
        self.keyToNum = {
            "C" : 52,
            "C#" : 53,
            "D" : 54,
            "D#" : 55,
            "E" : 56,
            "F" : 57,
            "F#" : 58,
            "G" : 59,
            "G#" : 60,
            "A" : 61,
            "A#" : 62,
            "B" : 63
        }
        self.posToKey = {
            10: "C5"
        }
    
    def play(self, pos, image_height, image_width):
        print(pos)
        if(pos[0] < image_width/2):
            print("D")
            self.play_key("D5")
        else:
            print("G")
            self.play_key("G5")

    def play_key(self, key):
        key_num = self.keyToNum[key[0]] + (key[1] == "#") + (int(key[-1])-5)*12
        print(key_num)
        self.piano.record_key(key_num, duration=0.3)
        self.piano.play()
    
    def __del__(self):
        print("Program Finished")
        self.piano.close()


if __name__ == "__main__":
    piano = Piano()
    piano.play("C#4")
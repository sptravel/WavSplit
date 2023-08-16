import os
import sys
import json

class AsrResult(object):
    def __init__(self, save_wave_path, save_text_path):
        self.wav_path = ""
        self.result = ""
        self.wav_list = []
        self.save_wave_path = save_wave_path
        self.save_text_path = save_text_path
        return
    
    def analysis(self, result_str):
        try:
            results = result_str.split(',', 1)
            self.wav_path = results[0].split('=')[1]
            result_json_str = results[1].split('=')[1]
            #print(result_json_str)
            self.result = json.loads(result_json_str)
            valid_data_list = self.result['data']
            max_valid_length = len(valid_data_list)
            for i in range(0, max_valid_length):
                self.wav_list.append((valid_data_list[i]['begin'], valid_data_list[i]['end'], valid_data_list[i]['transcript']))   
            return 1
        except:
            print("json.loads error, result_json_str is %s\n"%result_json_str)
            self.wav_list.clear()
            return -1
    
    def reset(self, result_str):
        self.wav_list.clear()
        self.analysis(result_str)


    def process(self):
        wav_name = self.wav_path.split('/')[-1].split('.')[0]
        wav_folder = self.save_wave_path + '/' + wav_name
        f1 = open(self.save_text_path, 'a', encoding='utf-8')
        if not os.path.exists(wav_folder):
            os.makedirs(wav_folder)
        for i in self.wav_list:
            tmp_save_path = wav_folder + "/" + "wav_name_%d_%d"%(i[0], i[1])
            #print('ffmpeg -i %s -codec copy -ss %f -t %f %s.wav'%(self.wav_path, float(i[0])/1000, float(i[1])/1000, tmp_save_path))
            os.system('ffmpeg -i %s -codec copy -ss %f -t %f -y %s.wav'%(self.wav_path, float(i[0])/1000, float(i[1])/1000, tmp_save_path))
            f1.write('%s:%s\n'%(tmp_save_path, i[2]))
        f1.close()


def split_ar_result(log_path, save_wave_path, save_text_path):
    log_lines = read_lines(log_path)
    asr_tools = AsrResult(save_wave_path, save_text_path)
    for line in log_lines:
        asr_tools.reset(line)
        asr_tools.process()


def read_lines(in_path):
    f1 = open(in_path, 'r', encoding='utf-8')
    f1_lines=f1.readlines()
    return f1_lines


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('error\nusage: python %s log_path, save_wave_path, save_text_path' % sys.argv[0])
        exit(1)
    split_ar_result(sys.argv[1], sys.argv[2], sys.argv[3])



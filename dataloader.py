from glob import glob
import numpy as np
import os
from scipy.io.wavfile import read, write
from scipy.signal import resample


class DataGenerator:
    def __init__(self, fileList, time_sec=60) -> None:
        self.fileList = fileList
        self.timeSec = time_sec
        self.fileProgress = 0
        self.listProgress = 0
        self.fileEnd = False
        self.listEnd = False
        self.fileIdx = 0
        self.listIdx = 0
        self.fs, self.data = read(self.fileList[self.listIdx])
        self.prevMinutes = 0
    
    def getData(self, down_rate):
        if self.listEnd == True:  # 列表已空，代表没有数据可读
            print('list over!!!')
            return 0, np.zeros(shape=(1,))
        # 还有数据可以读
        if self.fileIdx == 0:
            self.prevMinutes = 0
        if self.fileIdx+self.fs*self.timeSec < self.data.size:
            # 数据还够一帧
            temp = self.data[self.fileIdx:self.fileIdx+self.fs*self.timeSec]
            self.fileEnd = False
            self.fileIdx += self.fs*self.timeSec
            self.prevMinutes += 1
            self.fileProgress = int(100*(self.fileIdx+1)//self.data.size)
        else:  # 当前文件不够一帧，已到末尾
            temp = self.data[self.fileIdx:]
            self.prevMinutes += 1
            if len(self.fileList) == self.listIdx+1:  # 若文件没有下一个了，列表遍历结束
                self.listEnd = True
            else:  # 还有下一个文件
                self.listIdx += 1
                self.fileIdx = 0
                self.fs, self.data = read(self.fileList[self.listIdx])

            self.fileProgress = 100
            self.fileEnd = True
        self.listProgress = int(100*(self.listIdx+1)//len(self.fileList))
        return self.fs//down_rate, self.downSample(temp, down_rate)

    def getFileName(self):
        return self.fileList[self.listIdx]

    def getFileIdx(self):
        return self.fileIdx

    def downSample(self, data, rate):
        if rate == 1:
            return data
        else:
            idx = np.arange(0, len(data), rate)
            tmp = data[idx]
            return tmp

    # def downSample(self, data, rate):
    #     if rate == 1:
    #         return data
    #     else:
    #         tmp = resample(data, len(data)//rate)
    #         return tmp

    def isListEnd(self):
        return self.listEnd

    def isFileEnd(self):
        return self.fileEnd

    def listPg(self):
        return self.listProgress

    def filePg(self):
        return self.fileProgress

    def saveDat(self,fileDir,data,fs,idx):
        if not os.path.exists('Process done'):
            os.mkdir('Process done')
        fileName = '.\\Process done\\'+fileDir.split('\\')[2]+str(idx)+'.wav'
        write(fileName,fs,data)

    def split_save_data(self, down_rate):
        i=0
        while True:
            if generator.isListEnd() == False:
                dir = generator.getFileName()
                print(i,dir)
                i+=1
                fs, data = generator.getData(down_rate)
                generator.saveDat(dir, data, fs, generator.prevMinutes-1)
                print(fs, data.shape, generator.listPg(), ' ', generator.filePg(
                ), generator.isFileEnd(), generator.isListEnd(), generator.prevMinutes-1)
            else:
                break




if __name__ == '__main__':
    fileLists = glob('.\\data\\*.wav')
    generator = DataGenerator(fileLists, 300)
    generator.split_save_data(down_rate=12)
    # i=0
    # while True:
    #     if generator.isListEnd() == False:
    #         dir = generator.getFileName()
    #         print(i,dir)
    #         i+=1
    #         fs, data = generator.getData(down_rate=12)
    #         generator.saveDat(dir, data, fs, generator.prevMinutes-1)
    #         print(fs, data.shape, generator.listPg(), ' ', generator.filePg(
    #         ), generator.isFileEnd(), generator.isListEnd(), generator.prevMinutes-1)
    #     else:
    #         break

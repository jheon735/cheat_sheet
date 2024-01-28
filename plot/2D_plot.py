import numpy as np
import matplotlib.pyplot as plt

class plot:
    def sigle_2d(self, x, y, values, value_name,  pcmap = None, save_opt = False, save_name = None):
        """
        단일 그래프 생산
        :param x: value 와 같은 모양의 x좌표를 입력한 배열
        :param y: value와 같은 모양의 y좌표를 입력한 배열
        :param values: 2차원 배열
        :param pcmap : 사용할 cmap, None일 경우 min-max 사용
        :param save_opt: 저장 옵션. True일 경우 save_name을 받아 파일 저장
        :param save_name: 경로까지 포함한 파일 이름
        :return: 없음
        """
        fig = plt.figure()

        if pcmap == None:
            cmap = plt.cm.jet
            norm = None
        else:
            cmap, norm = self.make_cmap(pcmap)

        ax1 = plt.subplot(111)
        c = ax1.pcolormesh(x, y, values, cmap=cmap, norm = norm)
        plt.title(f'{value_name}')
        ax1.set_aspect('equal', 'box')
        ax1.axis([x.min(), x.max(), y.min(), y.max()])
        ax1.set_yticks([])
        ax1.set_xticks([])
        fig.colorbar(c, ax=ax1, norm=norm)

        plt.tight_layout()
        if save_opt:
            plt.savefig(f'{save_name}')
        else:
            plt.show()
        plt.close()


    def compare_2d(self, x, y, value1, value2, pcmap = None, val1_name = None, val2_name = None, save_opt = False, save_name = None):
        """
        두 그래프의 비교를 그래는 함수
        value1과 value2는 같은 모양의 2차원 배열이여야 한다
        :param x: value 와 같은 모양의 x좌표를 입력한 배열
        :param y: value와 같은 모양의 y좌표를 입력한 배열
        :param value1: 2차원 배열
        :param value2: 2차원 배열
        :param val1_name: 그림 title로 사용할 이름
        :param val2_name: 그림 title로 사용할 이름
        :param save_opt: 저장 옵션 True일 경우 아래 save_name의 이름으로 저장
        :param save_name: 경로를 포함한 저장할 파일 이름
        :return:
        """
        avg_differ = np.mean(value1-value2)
        std_differ = np.std(value1-value2)

        fig = plt.figure(figsize = (16, 4.5))

        if pcmap == None:
            cmap = plt.cm.jet
            norm = None
        else:
            cmap, norm = self.make_cmap(pcmap)

        ax1 = plt.subplot(131)
        c = ax1.pcolormesh(x, y, value1, cmap=cmap, norm = norm)
        if val1_name:
            plt.title(f'{val1_name}')
        ax1.axis([x.min(), x.max(), y.min(), y.max()])
        ax1.set_yticks([])
        ax1.set_xticks([])
        fig.colorbar(c, ax=ax1)#, norm=norm)

        ax2 = plt.subplot(132)
        c = ax2.pcolormesh(x, y, value2, cmap=cmap, norm = norm)
        ax2.axis([x.min(), x.max(), y.min(), y.max()])
        ax2.set_yticks([])
        ax2.set_xticks([])
        if val2_name:
            plt.title(f'{val2_name}')
        fig.colorbar(c, ax=ax2)#, norm = norm)

        ax3 = plt.subplot(133)
        c = ax3.pcolormesh(x, y, value1 - value2, cmap=cmap)#, norm = norm)
        plt.text(-230000, 200000, 'mean = %0.1f\nstd=%0.2f'%(avg_differ, std_differ))
        if val1_name:
            plt.title(f'{val1_name} - {val2_name}')
        ax3.axis([x.min(), x.max(), y.min(), y.max()])
        ax3.set_yticks([])
        ax3.set_xticks([])
        fig.colorbar(c, ax=ax3)#, norm = norm)
        plt.tight_layout()

        if save_opt:
            plt.savefig(f'{save_name}')
        else:
            plt.show()
        plt.close()
# -*- coding: utf-8 -*-
"""
Created on Wed 15 Mar 2023
@author: Juheon Lee 10th overwintering space scientist
"""
import ftplib
import os
from ftplib import FTP
import pysftp
from datetime import datetime, timedelta
import configparser
from pathlib import Path
import logging

config_file = 'ipinfo.ini'

config = configparser.ConfigParser()
config.read(config_file, encoding='utf-8')
log_dir = './backup_log.txt'

log_format = logging.Formatter('%(asctime)s %(lineno)4d %(levelname)8s:%(message)s')
logging.basicConfig(format='%(asctime)s %(lineno)4d %(levelname)8s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(log_dir)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

class backup:
    def __init__(self, backup_time): #0시 0분 데이터 입력 추천
        self.btime = backup_time

    def ftp_download_hourly(self, log_name, ip, id, pw, local, remote): #폴더가 hour단위인 경우
        tt = self.btime
        logger.info(f"\t{log_name} Backup Start")
        count = 0
        with FTP(ip) as ftp:
            ftp.login(id, pw)
            ftp.set_pasv(False)
            logger.info(f"\t\t{log_name} Connection Success")

            ddts = [tt + timedelta(hours=i) for i in range(24)]
            for dt in ddts:
                ldir = Path(f'{local}/{dt.strftime("%Y")}/{dt.strftime("%m")}/{dt.strftime("%d")}/{dt.strftime("%H")}')
                rdir = f'{remote}/{dt.strftime("%Y")}/{dt.strftime("%m")}/{dt.strftime("%d")}/{dt.strftime("%H")}'

                try:
                    ftp.cwd(rdir)  # hour 데이터 먼저
                    files = ftp.nlst()

                    if len(files) == 0:
                        logger.info("\t\tNo file in remote path")
                        continue

                    if not os.path.isdir(ldir):
                        os.makedirs(ldir)

                    local_flist = os.listdir(ldir)
                    for fname in files:
                        if fname in local_flist:
                            pass
                        else:
                            with open(ldir / fname, 'wb') as f:
                                ftp.retrbinary('RETR ' + fname, f.write)
                            count += 1

                except IOError:
                    continue
                except ftplib.error_perm:
                    continue

            logger.info(f'\t\ttotal {count} {dt.strftime("%Y%m%d")} {log_name} downloaded')

        logger.info(f"\t{log_name} Backup Finished")

    def ftp_download_directory(self, log_name, ip, id, pw, local, remote): #폴더 전체 다운로드
        dt = self.btime
        logger.info(f"\t{log_name} Backup Start")
        with FTP(ip) as ftp:
            ftp.login(id, pw)
            ftp.set_pasv(False)
            logger.info(f"\t\t{log_name} Connection Success")

            count = 0
            try:
                ftp.cwd(remote)
                files = ftp.nlst()
                if len(files) == 0:
                    logger.info("\t\tNo file in remote path")
                    return True

                if not os.path.isdir(local):
                    os.makedirs(local)

                local_flist = os.listdir(local)
                for fname in files:
                    if fname in local_flist:
                        pass
                    else:
                        with open(local / fname, 'wb') as f:
                            ftp.retrbinary('RETR ' + fname, f.write)
                        count += 1
                logger.info(f'\t\ttotal {count} {dt.strftime("%Y%m%d")} {log_name} downloaded')

            except ftplib.error_perm:
                logger.info(f'\t\tNo directory on {dt.strftime("%Y%m%d")}')

        logger.info(f"\t{log_name} Backup Finished")

    def sftp_download_directory(self, log_name, ip, id, pw, local, remote): #폴더 전체 백업
        nt = datetime.utcnow()
        logger.info(f"\t{log_name} Backup Start")
        with pysftp.Connection(ip, username=id, password=pw) as sftp:
            logger.info('\t\tConnection Success')
            try:
                count = 0
                if sftp.isdir(remote) == True:
                    with sftp.cd(remote):
                        files = sftp.listdir()
                        if len(files) == 0:
                            logger.info("\t\tNo file in remote path")
                            return True

                        if not os.path.isdir(local):
                            os.makedirs(local)

                        local_flist = os.listdir(local)
                        for fname in files:
                            if fname in local_flist:
                                pass
                            else:
                                info = sftp.stat(fname)
                                mt = datetime.utcfromtimestamp(info.st_mtime)
                                if abs(nt - mt) > timedelta(minutes=5):
                                    sftp.get(fname, localpath=local / fname)
                                    count += 1
                        logger.info(f'\t\ttotal {count} {self.btime.strftime("%Y%m%d")} {log_name} downloaded')

            except IOError:
                logger.info(f'\t\tNo data on {self.btime.strftime("%Y%m%d")}')

    def ftp_download_byname(self, log_name, ip, id, pw, local, remote, fname):
        nt = datetime.utcnow()
        logger.info(f"\t{log_name} Backup Start")

        if not os.path.isdir(local):
            os.makedirs(local)

        with FTP(ip) as ftp:
            ftp.login(id, pw)
            ftp.set_pasv(False)
            logger.info(f"\t\t{log_name} Connection Success")
            ftp.cwd(remote)  # hour 데이터 먼저
            files = ftp.nlst()

            if not fname in files:
                logger.info("\t\tNo file in remote path")
                return True

            mod_time = ftp.voidcmd('MDTM ' + fname)[4:]
            mt = datetime.strptime(mod_time, '%Y%m%d%H%M%S')
            if abs(nt - mt) > timedelta(minutes=5):
                with open(local / fname, 'wb') as f:
                    ftp.retrbinary('RETR ' + fname, f.write)
                logger.info('\t\t%s downloaded' % fname)
            else:
                logger.info('\t\tThe file is being used. Cannot Download')

        logger.info(f"\t{log_name} Backup Finished")

    def sftp_download_byname(self, log_name, ip, id, pw, local, remote, fname):
        nt = datetime.utcnow()
        logger.info(f"\t{log_name} Backup Start")

        if not os.path.isdir(local):
            os.makedirs(local)

        with pysftp.Connection(ip, username=id, password=pw) as sftp:
            logger.info('\t\tConnection Success')
            with sftp.cd(remote):
                files = sftp.listdir()

                if not fname in files:
                    logger.info("\t\tNo file in remote path")
                    return True

                info = sftp.stat(fname)
                mt = datetime.utcfromtimestamp(info.st_mtime)
                if abs(nt - mt) > timedelta(minutes=5):
                    sftp.get(fname, localpath=local / fname)
                    logger.info('\t\t%s downloaded' % fname)
                else:
                    logger.info('\t\tThe file is being used. Cannot Download')

        logger.info(f"\t{log_name} Backup Finished")

    def vipir_ionogram_backup(self, log_name, ip, id, pw, local, remote, days=3):
        logger.info(f"\t{log_name} Backup Start")

        with pysftp.Connection(ip, username=id, password=pw) as sftp:
            logger.info('\t\tConnection Success')
            dts = [self.btime - timedelta(days=i) for i in range(days)]
            for dt in dts:
                remd = f"{remote}/{dt.strftime('%j')}/ionogram"
                locd = local / dt.strftime('%j') / 'ionogram'

                if not os.path.isdir(locd):
                    os.makedirs(locd)

                try:
                    count = 0

                    if sftp.isdir(remd):
                        with sftp.cd(remd):
                            files = sftp.listdir()
                            if len(files) == 0:
                                logger.info("\t\tNo file in remote path")
                                return True

                            local_flist = os.listdir(locd)
                            for fname in files:
                                if fname in local_flist or fname.split('.')[-1] == 'ngi':
                                    pass
                                else:
                                    info = sftp.stat(fname)
                                    mt = datetime.utcfromtimestamp(info.st_mtime)
                                    if abs(datetime.utcnow() - mt) > timedelta(minutes=5):
                                        sftp.get(fname, localpath=locd / fname)
                                        count += 1
                            logger.info(f'\t\ttotal {count} {dt.strftime("%j")} individual ionogram downloaded')

                except IOError:
                    logger.info(f'\t\tNo data on {self.btime.strftime("%Y%m%d")}')

        logger.info(f"\t{log_name} Backup Finished")

def backup_JBS():
    ut_now = datetime.utcnow()
    # ut_now = datetime(2023, 5, 12)
    dt = datetime(ut_now.year, ut_now.month, ut_now.day)-timedelta(days=1)
    bu = backup(dt)

    logger.info(f"{dt.strftime('%Y%m%d')} data backup start")
    # NM Main
    ip = config['NM_main']['ip']
    id = config['NM_main']['id']
    pw = config['NM_main']['pw']
    local_dir = Path(config['NM_main']['local_path'])
    remote_dir = Path(config['NM_main']['remote_path'])

    # Hour data
    hour_dir = local_dir / 'Hour'
    chfname = dt.strftime('JBS_%y_%m_%d_1H.TXT')
    bu.ftp_download_byname('NM_main_corr_hour', ip, id, pw, hour_dir, str(remote_dir/'Hour'), chfname)

    # Minute data
    min_dir = local_dir / 'Minute'
    cmfname = dt.strftime('JBS_%y_%m_%d_1m.TXT')
    bu.ftp_download_byname('NM_main_corr_min', ip, id, pw, min_dir, str(remote_dir/'Minute'), cmfname)

    # NM Backup
    ip = config['NM_backup']['ip']
    id = config['NM_backup']['id']
    pw = config['NM_backup']['pw']
    local_dir = Path(config['NM_backup']['local_path'])
    remote_dir = Path(config['NM_backup']['remote_path'])

    # Hour data
    bhour_dir = local_dir / 'HourData'
    bhfname = dt.strftime('JBS_%y_%m_%d.LOG')
    bu.ftp_download_byname('NM_backup_raw_hour', ip, id, pw, bhour_dir, str(remote_dir/'HourData'), bhfname)

    # Minute data
    bmin_dir = local_dir / 'MinuteData'
    bmfname = dt.strftime('JBS_%y_%m_%d.DAT')
    bu.ftp_download_byname('NM_backup_raw_min', ip, id, pw, bmin_dir, str(remote_dir/'MinuteData'), bmfname)
    logger.info("\n")
    #Fluxgate Backup
    ip = config['fluxgate']['ip']
    id = config['fluxgate']['id']
    pw = config['fluxgate']['pw']
    local_dir = Path(config['fluxgate']['local_path'])
    remote_dir = Path(config['fluxgate']['remote_path'])

    fname = dt.strftime('%Y%m%d.txt')
    bu.ftp_download_byname('Fluxgate', ip, id, pw, local_dir, str(remote_dir), fname)
    logger.info("\n")
    #SCM Backup
    ip = config['SCM']['ip']
    id = config['SCM']['id']
    pw = config['SCM']['pw']
    local_dir = Path(config['SCM']['local_path'])
    remote_dir = config['SCM']['remote_path']

    fname = dt.strftime('%Y%m%d.txt')
    bu.sftp_download_byname('SCM', ip, id, pw, local_dir / dt.strftime('%Y'), remote_dir, fname)
    logger.info("\n")
    #Aurora-ASC Backup
    ip = config['AASC']['ip']
    id = config['AASC']['id']
    pw = config['AASC']['pw']
    local_dir = Path(config['AASC']['local_path'])
    remote_dir = Path(config['AASC']['remote_path'])

    #raw data
    bu.ftp_download_hourly('AuroraASC_raw_image', ip, id, pw, local_dir, str(remote_dir / 'ASC_img'))
    #processed data
    pro_dir = local_dir / 'AASC_processed' / dt.strftime("%Y") / dt.strftime("%m") / dt.strftime("%d")
    pro_rdir = remote_dir / 'ASC_processed' / dt.strftime("%Y") / dt.strftime("%m") / dt.strftime("%d")
    bu.ftp_download_directory('AuroraASC_processed_image', ip, id, pw, pro_dir, str(pro_rdir))
    logger.info("\n")
    #Filter-ASC Backup
    ip = config['FASC']['ip']
    id = config['FASC']['id']
    pw = config['FASC']['pw']
    local_dir = Path(config['FASC']['local_path'])
    remote_dir = Path(config['FASC']['remote_path'])

    #raw data
    bu.ftp_download_hourly('FilterASC_raw_image', ip, id, pw, local_dir, str(remote_dir))
    #processed data
    pro_dir = local_dir / 'sample_data' / dt.strftime("%Y") / dt.strftime("%m") / dt.strftime("%d")
    pro_rdir = remote_dir / 'sample_data' / dt.strftime("%Y") / dt.strftime("%m") / dt.strftime("%d")
    bu.ftp_download_directory('FilterASC_processed_image', ip, id, pw, pro_dir, str(pro_rdir))
    logger.info("\n")
    #KASI-ASC Backup
    ip = config['KASC']['ip']
    id = config['KASC']['id']
    pw = config['KASC']['pw']
    local_dir = Path(config['KASC']['local_path'])
    remote_dir = Path(config['KASC']['remote_path'])
    bu.ftp_download_hourly('KASIASC_raw_image', ip, id, pw, local_dir, str(remote_dir))
    logger.info("\n")
    #VIPIR Backup
    ip = config['VIPIR']['ip']
    id = config['VIPIR']['id']
    pw = config['VIPIR']['pw']
    local_dir = Path(config['VIPIR']['local_path']) / dt.strftime("%Y")
    remote_dir1 = config['VIPIR']['remote_path1']
    remote_dir2 = config['VIPIR']['remote_path2']

    #daily misc
    dmisc_loc = local_dir / 'daily' / dt.strftime('%j') / 'misc'
    dmisc_rem1 = f"{remote_dir1}/daily/{dt.strftime('%Y')}/{dt.strftime('%j')}/misc"
    bu.sftp_download_directory('VIPIR_daily_misc_data1', ip, id, pw, dmisc_loc, dmisc_rem1)
    dmisc_rem2 = f"{remote_dir2}/daily/{dt.strftime('%Y')}/{dt.strftime('%j')}/misc"
    bu.sftp_download_directory('VIPIR_daily_misc_data2', ip, id, pw, dmisc_loc, dmisc_rem2)

    #daily image
    dimage_loc = local_dir / 'daily' / dt.strftime('%j') / 'image'
    dimage_rem1 = f"{remote_dir1}/daily/{dt.strftime('%Y')}/{dt.strftime('%j')}/image"
    bu.sftp_download_directory('VIPIR_daily_image_data1', ip, id, pw, dimage_loc, dimage_rem1)
    dimage_rem2 = f"{remote_dir2}/daily/{dt.strftime('%Y')}/{dt.strftime('%j')}/image"
    bu.sftp_download_directory('VIPIR_daily_imgae_data2', ip, id, pw, dimage_loc, dimage_rem2)

    #individual image
    iimage_loc = local_dir / 'individual' / dt.strftime('%j') / 'image'
    iimage_rem1 = f"{remote_dir1}/individual/{dt.strftime('%Y')}/{dt.strftime('%j')}/image"
    bu.sftp_download_directory('VIPIR_individual_image1', ip, id, pw, iimage_loc, str(iimage_rem1))
    iimage_rem2 = f"{remote_dir2}/individual/{dt.strftime('%Y')}/{dt.strftime('%j')}/image"
    bu.sftp_download_directory('VIPIR_individual_image2', ip, id, pw, iimage_loc, str(iimage_rem2))

    #individual ionogram
    iiono_loc = local_dir / 'individual'
    iiono_rem1 = f"{remote_dir1}/individual/{dt.strftime('%Y')}"
    bu.vipir_ionogram_backup('VIPIR_indiviaul_ionogram1', ip, id, pw, iiono_loc, iiono_rem1)
    iiono_rem2 = f"{remote_dir2}/individual/{dt.strftime('%Y')}"
    bu.vipir_ionogram_backup('VIPIR_indiviaul_ionogram2', ip, id, pw, iiono_loc, iiono_rem2)

    logger.info(f"{dt.strftime('%Y%m%d')} data backup finished")
    logger.info("\n")
    logger.info("\n")

if __name__ == "__main__":
    backup_JBS()

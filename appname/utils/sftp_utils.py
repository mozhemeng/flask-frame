import paramiko
import pathlib

from appname.log import logger


def sftp_upload(server_info, upload_list):
    try:
        transport = paramiko.Transport(server_info['host'], server_info['port'])
        transport.banner_timeout = 200
        transport.connect(username=server_info['username'],
                          password=server_info['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        for upload_file in upload_list:
            logger.info("start to put {}".format(upload_file['file_path']))
            sftp_mkdir_p(sftp, upload_file['remote_dir'])
            remote_path = str(pathlib.Path(upload_file['remote_dir']).joinpath(upload_file['remote_file_name']).absolute())
            sftp.put(upload_file['file_path'], remote_path)
            logger.info("success to put {}".format(upload_file['file_path']))
    except Exception as e:
        logger.error("failed to upload sftp with error: {}".format(e))
    finally:
        sftp.close()
        transport.close()


def sftp_mkdir_p(sftp_client, target_file_dir):
    target_file_dir = pathlib.Path(target_file_dir)
    parents = list(target_file_dir.parents)
    parents.reverse()
    parents.append(target_file_dir)
    for file_dir in parents:
        try:
            sftp_client.chdir(str(file_dir))
        except IOError:
            sftp_client.mkdir(str(file_dir))

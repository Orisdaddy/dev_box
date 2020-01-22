from paramiko import SFTPClient
from paramiko.sftp_attr import SFTPAttributes
from io import BytesIO


class IoSftpClient(SFTPClient):
    def put(self, content, file_size, remotepath, callback=None, confirm=True):
        bio = BytesIO(content)
        return self.putfo(bio, remotepath, file_size, callback, confirm)

    def putfo(self, fl, remotepath, file_size=0, callback=None, confirm=True):
        with self.file(remotepath, "wb") as fr:
            fr.set_pipelined(True)
            size = self._transfer_with_callback(
                reader=fl, writer=fr, file_size=file_size, callback=callback
            )
        if confirm:
            s = self.stat(remotepath)
            if s.st_size != size:
                raise IOError(
                    "size mismatch in put!  {} != {}".format(s.st_size, size)
                )
        else:
            s = SFTPAttributes()
        return s

    def get(self, remotepath, callback=None):
        bio = BytesIO()
        f = self.getfo(remotepath, bio, callback)
        content = f.getvalue()
        return content

    def getfo(self, remotepath, fl, callback=None):
        file_size = self.stat(remotepath).st_size
        with self.open(remotepath, "rb") as fr:
            fr.prefetch(file_size)
            return self._transfer_with_callback(
                reader=fr, writer=fl, file_size=file_size, callback=callback
            )

    def _transfer_with_callback(self, reader, writer, file_size, callback):
        size = 0
        while True:
            data = reader.read(32768)
            writer.write(data)
            size += len(data)
            if len(data) == 0:
                break
            if callback is not None:
                callback(size, file_size)
        if isinstance(writer, BytesIO):
            return writer
        else:
            return size
